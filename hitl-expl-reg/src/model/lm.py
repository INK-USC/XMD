import os, pickle, warnings
from typing import Optional, List
from timeit import default_timer as timer

import torch
from torch import nn
import torch.nn.functional as F
from torch.nn.utils.rnn import pad_sequence

from hydra.utils import instantiate, get_original_cwd
from omegaconf import DictConfig

from transformers import AutoModel, AutoTokenizer

from src.model.base_model import BaseModel
from src.model.mlp import MLP_factory
from src.utils.data import dataset_info
from src.utils.losses import calc_task_loss, calc_pos_expl_loss, calc_neg_expl_loss
from src.utils.metrics import init_best_metrics, init_perf_metrics, calc_preds
from src.utils.expl import attr_algos, baseline_required
from src.utils.optim import setup_optimizer_params, setup_scheduler, freeze_layers
from src.utils.logging import log_step_losses, log_step_metrics, log_epoch_losses, log_epoch_metrics


class LanguageModel(BaseModel):
    def __init__(self,
                 arch: str, dataset: str, optimizer: DictConfig, num_classes: int,
                 scheduler: DictConfig, num_freeze_layers: int = 0, freeze_epochs=-1, neg_weight=1,
                 expl_reg: bool = False, expl_reg_freq: int = 1, task_wt: float = None, attr_algo: str = None,
                 pos_expl_wt: float = 0.0, pos_expl_criterion: str = None, pos_expl_margin: float = None,
                 neg_expl_wt: float = 0.0, neg_expl_criterion: str = None, neg_expl_margin: float = None,
                 ig_steps: int = 3, internal_batch_size: int = None, gradshap_n_samples: int = 3, gradshap_stdevs: float = 0.0,
                 compute_attr: bool = False, save_outputs: bool = False, exp_id: str = None, attr_scaling: float = 1,
                 **kwargs):

        super().__init__()

        self.save_hyperparameters()

        self.arch = arch
        self.dataset = dataset
        self.optimizer = optimizer
        self.num_classes = num_classes
        self.max_length = dataset_info[dataset]['max_length'][arch]

        self.scheduler = scheduler
        self.freeze_epochs = freeze_epochs
        self.neg_weight = neg_weight

        self.expl_reg = expl_reg
        self.expl_reg_freq = expl_reg_freq
        self.task_wt = task_wt
        
        self.pos_expl_wt = pos_expl_wt
        self.pos_expl_criterion = pos_expl_criterion
        self.pos_expl_margin = pos_expl_margin

        self.neg_expl_wt = neg_expl_wt
        self.neg_expl_criterion = neg_expl_criterion
        self.neg_expl_margin = neg_expl_margin

        self.best_metrics = init_best_metrics()
        self.perf_metrics = init_perf_metrics(num_classes)

        self.compute_attr = compute_attr
        assert attr_algo in list(attr_algos.keys()) + [None]
        self.attr_algo = attr_algo
        
        self.task_encoder = AutoModel.from_pretrained(arch)
        self.task_head = nn.Linear(
            self.task_encoder.config.hidden_size,
            num_classes if self.dataset != 'cose' else 1
        )
        self.model_dict = {
            'task_encoder': self.task_encoder,
            'task_head': self.task_head,
        }

        if self.expl_reg or self.compute_attr:
            self.attr_dict = {
                'attr_algo': attr_algo,
                'baseline_required': baseline_required[attr_algo],
                'attr_func': attr_algos[attr_algo](self),
                'tokenizer': AutoTokenizer.from_pretrained(arch),
            }
            if attr_algo == 'integrated-gradients':
                self.attr_dict['ig_steps'] = ig_steps
                self.attr_dict['internal_batch_size'] = internal_batch_size
            elif attr_algo == 'gradient-shap':
                self.attr_dict['gradshap_n_samples'] = gradshap_n_samples
                self.attr_dict['gradshap_stdevs'] = gradshap_stdevs

        assert num_freeze_layers >= 0
        if num_freeze_layers > 0:
            freeze_layers(self, num_freeze_layers)

        if save_outputs:
            assert exp_id is not None
        self.save_outputs = save_outputs
        self.exp_id = exp_id
        self.attr_scaling = attr_scaling
        

    def calc_attrs(self, input_ids, attn_mask, targets=None):
        # If dataset is CoS-E, use zeros as targets
        if self.dataset == 'cose':
            assert targets is None
            targets = torch.zeros(len(input_ids)).long().to(input_ids.device)

        # Compute input embs and baseline embs
        input_embeds, baseline_embeds = self.get_attr_func_inputs(
            input_ids,
            self.attr_dict['baseline_required'],
        )

        # Compute dim-level attrs via attr algo
        if self.attr_dict['attr_algo'] == 'integrated-gradients':
            attrs = self.attr_dict['attr_func'].attribute(
                inputs=input_embeds.requires_grad_(), baselines=baseline_embeds,
                target=targets, additional_forward_args=(attn_mask, 'captum'),
                n_steps=self.attr_dict['ig_steps'], internal_batch_size=self.attr_dict['internal_batch_size'],
            ).float()
        elif self.attr_dict['attr_algo'] == 'gradient-shap':
            attrs = self.attr_dict['attr_func'].attribute(
                inputs=input_embeds.requires_grad_(), baselines=baseline_embeds,
                target=targets, additional_forward_args=(attn_mask, 'captum'),
                n_samples=self.attr_dict['gradshap_n_samples'], stdevs=self.attr_dict['gradshap_stdevs'],
            ).float()

        elif self.attr_dict['attr_algo'] == 'deep-lift':
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                attrs = self.attr_dict['attr_func'].attribute(
                    inputs=input_embeds.requires_grad_(), baselines=baseline_embeds,
                    target=targets, additional_forward_args=(attn_mask, 'captum'),
                ).float()
        elif self.attr_dict['attr_algo'] in ['input-x-gradient', 'saliency']:
            attrs = self.attr_dict['attr_func'].attribute(
                inputs=input_embeds.requires_grad_(),
                target=targets, additional_forward_args=(attn_mask, 'captum'),
            ).float()

        # Pool dim-level attrs into token-level attrs
        attrs = torch.sum(attrs, dim=-1)

        # Mask out attrs for non-pad tokens
        attrs = attrs * attn_mask

        # Make sure no attr scores are NaN
        assert not torch.any(torch.isnan(attrs))

        return attrs

    def get_attr_func_inputs(self, input_ids, baseline_required):
        word_emb_layer = self.task_encoder.embeddings.word_embeddings
        tokenizer = self.attr_dict['tokenizer']
        input_embeds = word_emb_layer(input_ids)
        if baseline_required:
            baseline = torch.full(input_ids.shape, tokenizer.pad_token_id, device=input_ids.device).long()
            baseline[:, 0] = tokenizer.cls_token_id
            sep_token_locs = torch.nonzero(input_ids == tokenizer.sep_token_id)
            baseline[sep_token_locs[:, 0], sep_token_locs[:, 1]] = tokenizer.sep_token_id
            baseline_embeds = word_emb_layer(baseline)
        else:
            baseline_embeds = None
        return input_embeds, baseline_embeds

    def forward(self, inputs, attention_mask, mode='task'):
        assert mode in ['task', 'captum']
        if mode == 'task':
            enc = self.task_encoder(input_ids=inputs, attention_mask=attention_mask).pooler_output
            logits = self.task_head(enc)
            if self.dataset == 'cose':
                logits = logits.reshape(-1, self.num_classes)
        elif mode == 'captum':
            enc = self.task_encoder(inputs_embeds=inputs, attention_mask=attention_mask).pooler_output
            logits = self.task_head(enc)

        return logits

    def attr_forward(self, input_ids, attn_mask):
        if self.dataset == 'cose':
            return self.calc_attrs(input_ids, attn_mask)
        else:
            batch_size = input_ids.shape[0]
            input_ids_ = input_ids.unsqueeze(1).expand(-1, self.num_classes, -1).reshape(-1, self.max_length)
            attn_mask_ = attn_mask.unsqueeze(1).expand(-1, self.num_classes, -1).reshape(-1, self.max_length)
            all_classes = torch.arange(self.num_classes).to(input_ids.device).unsqueeze(0).expand(batch_size, -1).flatten()
            return self.calc_attrs(input_ids_, attn_mask_, all_classes).reshape(batch_size, self.num_classes, self.max_length)

    def run_step(self, batch, split, batch_idx):
        input_ids = batch['input_ids']
        attn_mask = batch['attention_mask']
        rationale = batch['rationale']
        has_rationale = batch['has_rationale']
        targets = batch['label']
        batch_size = len(input_ids)

        if self.dataset == 'cose':
            input_ids = input_ids.reshape(-1, self.max_length)
            attn_mask = attn_mask.reshape(-1, self.max_length)
            rationale = rationale.reshape(-1, self.max_length)
            has_rationale = has_rationale.reshape(-1)

        eval_split: str = batch['split']
        if split == 'train':
            assert split == eval_split
        ret_dict, loss_dict, metric_dict = {}, {}, {}

        do_expl_reg = self.expl_reg and (batch_idx % self.expl_reg_freq == 0)

        if do_expl_reg or self.compute_attr:

            # Compute attributions for all classes
            attrs = self.attr_forward(input_ids, attn_mask)

        # Compute predictions and losses
        if do_expl_reg:
            # Compute task logits
            logits = self.forward(input_ids, attn_mask)

            # Compute task loss
            task_loss = self.task_wt * calc_task_loss(logits, targets)

            # Initialize expl loss as zero
            expl_loss = torch.tensor(0.0).to(self.device)

            # Compute positive expl loss (w.r.t target class)
            if self.pos_expl_wt > 0:
                assert self.dataset not in ['amazon', 'yelp']
                if self.dataset != 'cose':
                    pos_classes = targets.unsqueeze(1).expand(-1, self.max_length).unsqueeze(1)
                    pos_attrs = torch.gather(attrs, dim=1, index=pos_classes).squeeze(1)
                pos_expl_loss = self.pos_expl_wt * calc_pos_expl_loss(
                    attrs=pos_attrs if self.dataset != 'cose' else attrs,
                    rationale=rationale,
                    attn_mask=attn_mask,
                    criterion=self.pos_expl_criterion,
                    margin=self.pos_expl_margin,
                    has_rationale=has_rationale,
                    attr_scaling=self.attr_scaling,
                )
                expl_loss += pos_expl_loss
                loss_dict['pos_expl_loss'] = pos_expl_loss
    
            # Compute negative expl loss (w.r.t. non-target classes)
            if self.neg_expl_wt > 0:
                assert self.dataset not in ['amazon', 'yelp', 'cose']
                neg_expl_loss = self.neg_expl_wt * calc_neg_expl_loss(
                    attrs=attrs,
                    attn_mask=attn_mask,
                    criterion=self.neg_expl_criterion,
                    targets=targets,
                    preds=calc_preds(logits),
                )
                expl_loss += neg_expl_loss
                loss_dict['neg_expl_loss'] = neg_expl_loss

            # Log expl loss
            loss_dict['expl_loss'] = expl_loss

            # Compute total loss
            loss = task_loss + expl_loss

        else:
            logits = self.forward(input_ids, attn_mask)
            task_loss = calc_task_loss(logits, targets)
            loss = task_loss

        loss_dict['task_loss'] = task_loss
        loss_dict['loss'] = loss

        # Log step losses
        ret_dict = log_step_losses(self, loss_dict, ret_dict, do_expl_reg, eval_split)
        ret_dict['logits'] = logits.detach()
        ret_dict['targets'] = targets.detach()
        ret_dict['eval_split'] = eval_split

        # Log step metrics
        ret_dict = log_step_metrics(self, metric_dict, ret_dict, eval_split)

        # Save attrs
        if self.compute_attr or do_expl_reg:
            ret_dict['attrs'] = attrs.detach()

        return ret_dict

    def aggregate_epoch(self, outputs, split, current_epoch=None):
        if split == 'train':
            splits = ['train']
        elif split == 'dev':
            splits = ['dev', 'test']
        elif split == 'test':
            splits = [outputs[0]['eval_split']]
        outputs_list = outputs if split == 'dev' else [outputs]
        
        for dataset_idx, eval_split in enumerate(splits):
            outputs = outputs_list[dataset_idx]
            log_epoch_losses(self, outputs, eval_split) # Log epoch losses
            log_epoch_metrics(self, outputs, eval_split) # Log epoch metrics
        # Save outputs to file            
        if self.save_outputs:
            out_dir = f'{get_original_cwd()}/../save/{self.exp_id}/model_outputs/{self.dataset}'
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)
            keys = ['preds', 'targets', 'logits']
            if self.expl_reg or self.compute_attr:
                keys.append('attrs')
            for dataset_idx, eval_split in enumerate(splits):
                outputs = outputs_list[dataset_idx]
                for key in keys:
                    if key == 'preds':
                        logits = torch.cat([x['logits'] for x in outputs])
                        out_data = calc_preds(logits)
                    else:
                        out_data = torch.cat([x[key] for x in outputs])
                    out_data = out_data.cpu().detach()
                    if current_epoch:
                        out_file = os.path.join(out_dir, f'{eval_split}_epoch_{current_epoch}_{key}.pkl')
                    else:
                        out_file = os.path.join(out_dir, f'{eval_split}_{key}.pkl')
                    print(out_file)
                    pickle.dump(out_data.squeeze(), open(out_file, 'wb'))

    def configure_optimizers(self):
        optimizer_params = setup_optimizer_params(self.model_dict, self.optimizer)
        self.optimizer['lr'] = self.optimizer['lr'] * self.trainer.world_size
        optimizer = instantiate(
            self.optimizer, params=optimizer_params,
            _convert_="partial"
        )
        if self.scheduler.lr_scheduler == 'linear_with_warmup':
            scheduler = setup_scheduler(self.scheduler, self.total_steps, optimizer)
            return [optimizer], [scheduler]
        elif self.lr_scheduler == 'fixed':
            return [optimizer]
        else:
            raise NotImplementedError