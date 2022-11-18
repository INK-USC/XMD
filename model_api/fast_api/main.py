import json
import os
import sys
import warnings
import requests
import time
import torch
from fastapi import FastAPI, BackgroundTasks
from fastapi import status

import fast_api_util_functions as util_f
import json_schema as schema

# sys.path.append('../../hitl-expl-reg/')
# print(sys.path)
# from src.model import lm as lm
from transformers import AutoTokenizer, AutoModel
from transformers import AutoModelForSequenceClassification, AutoConfig
from captum.attr import IntegratedGradients, GradientShap, InputXGradient, Saliency, DeepLift

from config import attr_algos, baseline_required, dataset_info

app = FastAPI()


@app.get("/test")
async def root():
    """
    Endpoint for testing FastAPI
    """
    return {"message": "Hello World"}


@app.post("/generate/expl", status_code=status.HTTP_201_CREATED)
async def start_expl_generation(captum_training_payload: schema.CaptumTrainingPayload, background_tasks: BackgroundTasks):
    """
        Endpoint hit by XMD tool's django api to initiate captum process

        input params: # dataset_path, pretrained_model_name_or_path, from_local

        output params:
        
    """
    from_local = captum_training_payload.from_local
    dataset = captum_training_payload.dataset
    pretrained_model_name_or_path = captum_training_payload.pretrained_model_name_or_path
    config = AutoConfig.from_pretrained(pretrained_model_name_or_path)
    
    print(from_local, dataset, pretrained_model_name_or_path)
    background_tasks.add_task(generate_captum_attr_background, config, dataset, pretrained_model_name_or_path)


async def generate_captum_attr_background(config, dataset, arch):
    """
    Captum API call to get attribution scores
    """
    start = time.time()


    ### DEPENDENCIES
    # params:
    # arch = arch
    # dataset = None
    # optimizer = 
    # scheduler = 
    num_classes = config.type_vocab_size
    attr_algo = 'integrated-gradients'
    dataset_type = 'hatexplain'
    max_length = 256
    

    # tokenize dataset
    tokenizer = AutoTokenizer.from_pretrained(arch) # Tokenizer Initialize
    text, labels = dataset.text, dataset.labels
    data = tokenizer(text, padding=True)
    input_ids, token_type_ids, attn_mask = data['input_ids'], data['token_type_ids'], data['attention_mask']
    print(input_ids, token_type_ids, attn_mask)
    input_ids = torch.tensor(input_ids)
    attn_mask = torch.tensor(attn_mask)
    print(input_ids, attn_mask)


    ### attr_forward(self, input_ids, attn_mask):
    ###
    batch_size = input_ids.shape[0]
    input_ids_ = input_ids.unsqueeze(1).expand(-1, num_classes, -1).reshape(-1, max_length)
    attn_mask_ = attn_mask.unsqueeze(1).expand(-1, num_classes, -1).reshape(-1, max_length)
    all_classes = torch.arange(num_classes).to(input_ids.device).unsqueeze(0).expand(batch_size, -1).flatten()
    input_ids, attn_mask = input_ids_, attn_mask_
    targets = all_classes

    ### get_attr_func_inputs(self, input_ids, baseline_required)
    ###
    word_emb_layer = AutoModel.from_pretrained(arch).embeddings.word_embeddings
    tokenizer = tokenizer
    input_embeds = word_emb_layer(input_ids)
    if baseline_required:
        baseline = torch.full(input_ids.shape, tokenizer.pad_token_id, device=input_ids.device).long()
        baseline[:, 0] = tokenizer.cls_token_id
        sep_token_locs = torch.nonzero(input_ids == tokenizer.sep_token_id)
        baseline[sep_token_locs[:, 0], sep_token_locs[:, 1]] = tokenizer.sep_token_id
        baseline_embeds = word_emb_layer(baseline)
    else:
        baseline_embeds = None


    ### calc_attrs(self, input_ids, attn_mask, targets=None)
    attr_dict = {
        'attr_algo': attr_algo,
        'baseline_required': baseline_required[attr_algo],
        'attr_func': attr_algos[attr_algo](self),
        'tokenizer': tokenizer,
    }
    ###
    if attr_dict['attr_algo'] == 'integrated-gradients':
        attrs = attr_dict['attr_func'].attribute(
            inputs=input_embeds.requires_grad_(), baselines=baseline_embeds,
            target=targets, additional_forward_args=(attn_mask, 'captum'),
            n_steps=attr_dict['ig_steps'], internal_batch_size=attr_dict['internal_batch_size'],
        ).float()
    elif attr_dict['attr_algo'] == 'gradient-shap':
        attrs = attr_dict['attr_func'].attribute(
            inputs=input_embeds.requires_grad_(), baselines=baseline_embeds,
            target=targets, additional_forward_args=(attn_mask, 'captum'),
            n_samples=attr_dict['gradshap_n_samples'], stdevs=attr_dict['gradshap_stdevs'],
        ).float()

    elif attr_dict['attr_algo'] == 'deep-lift':
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            attrs = attr_dict['attr_func'].attribute(
                inputs=input_embeds.requires_grad_(), baselines=baseline_embeds,
                target=targets, additional_forward_args=(attn_mask, 'captum'),
            ).float()
    elif attr_dict['attr_algo'] in ['input-x-gradient', 'saliency']:
        attrs = attr_dict['attr_func'].attribute(
            inputs=input_embeds.requires_grad_(),
            target=targets, additional_forward_args=(attn_mask, 'captum'),
        ).float()


    attrs = torch.sum(attrs, dim=-1)
    attrs = attrs * attn_mask
    assert not torch.any(torch.isnan(attrs))

    attrs.reshape(batch_size, num_classes, max_length)
    end = time.time()
    print(end - start)

    print(attrs)
    return attrs


    



    # return attrs

### make periodic post requests to django to update status of captum