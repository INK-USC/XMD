import getpass, logging, socket
from typing import Any, List
import torch
from omegaconf.dictconfig import DictConfig
from omegaconf.omegaconf import OmegaConf
from pytorch_lightning.loggers import NeptuneLogger
from src.utils.metrics import calc_preds, get_step_metrics, get_epoch_metrics

API_LIST = {
    "neptune": {
        'aarzchan': 'eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiIwZDJiNGE0Yi1hY2M4LTRmNDUtOWEwMC1mMjZjMDY4OTcyYTgifQ==',
        'aaron': 'eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiIwZDJiNGE0Yi1hY2M4LTRmNDUtOWEwMC1mMjZjMDY4OTcyYTgifQ==',
        'brihi': 'eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI5YWY2NzY2Zi1hYmM2LTQ1ZmEtYjQxNS1kNjAzMWYyZjY5ZTcifQ==',
        'ziyi':'eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiI4ZGM4NTNhOC1mOWIxLTQ0MGYtYWE4OC1jZThlZTAzZjNiZTIifQ==',
        'danny911kr':'eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiJiZDE2ZWEzYS04NDYxLTQ0N2QtOTgxNy0yYjZjNWZiYWI1YTUifQ=='
    },
}


def get_username():
    return getpass.getuser()

def flatten_cfg(cfg: Any) -> dict:
    if isinstance(cfg, dict):
        ret = {}
        for k, v in cfg.items():
            flatten: dict = flatten_cfg(v)
            ret.update({
                f"{k}/{f}" if f else k: fv
                for f, fv in flatten.items()
            })
        return ret
    return {"": cfg}

def get_logger(name=__name__, level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger

def get_neptune_logger(
    cfg: DictConfig, project_name: str,
    name: str, tag_attrs: List[str], log_db: str,
    offline: bool, logger: str,
):
    neptune_api_key = API_LIST["neptune"][get_username()]

    # flatten cfg
    args_dict = {
        **flatten_cfg(OmegaConf.to_object(cfg)),
        "hostname": socket.gethostname()
    }
    tags = tag_attrs
    if cfg.model.expl_reg:
        tags.append('expl_reg')

    tags.append(log_db)

    neptune_logger = NeptuneLogger(
        api_key=neptune_api_key,
        project_name=project_name,
        experiment_name=name,
        params=args_dict,
        tags=tags,
        offline_mode=offline,
    )

    try:
        # for unknown reason, must access this field otherwise becomes None
        print(neptune_logger.experiment)
    except BaseException:
        pass

    return neptune_logger

def log_data_to_neptune(model_class, data, data_name, data_type, suffix, split, ret_dict=None, topk=None, detach_data=True):
    if topk:
        for i, k in enumerate(topk):
            model_class.log(f'{split}_{data_name}_{k}_{data_type}_{suffix}', data[i].detach(), prog_bar=True, sync_dist=(split != 'train'))
            if ret_dict is not None:
                ret_dict[f'{data_name}_{k}_{data_type}'] = data[i].detach() if detach_data else data[i]
    else:
        data_key = 'loss' if f'{data_name}_{data_type}' == 'total_loss' else f'{data_name}_{data_type}'
        model_class.log(f'{split}_{data_key}_{suffix}', data.detach(), prog_bar=True, sync_dist=(split != 'train'))
        if ret_dict is not None:
            ret_dict[data_key] = data.detach() if detach_data else data
    
    return ret_dict

def log_step_losses(model_class, loss_dict, ret_dict, do_expl_reg, split):
    ret_dict = log_data_to_neptune(model_class, loss_dict['loss'], 'total', 'loss', 'step', split, ret_dict, topk=None, detach_data=False)
    ret_dict = log_data_to_neptune(model_class, loss_dict['task_loss'], 'task', 'loss', 'step', split, ret_dict, topk=None)
    if do_expl_reg:
        ret_dict = log_data_to_neptune(model_class, loss_dict['expl_loss'], 'expl', 'loss', 'step', split, ret_dict, topk=None)
    return ret_dict

def log_step_metrics(model_class, metric_dict, ret_dict, split):
    return ret_dict

def log_epoch_losses(model_class, outputs, split):
    loss = torch.stack([x['loss'] for x in outputs]).mean()
    task_loss = torch.stack([x['task_loss'] for x in outputs]).mean()
    log_data_to_neptune(model_class, loss, 'total', 'loss', 'epoch', split, ret_dict=None, topk=None)
    log_data_to_neptune(model_class, task_loss, 'task', 'loss', 'epoch', split, ret_dict=None, topk=None)
    if model_class.expl_reg:
        assert len([x.get('expl_loss') for x in outputs if x is not None]) > 0
        expl_loss = torch.stack([x.get('expl_loss') for x in outputs if x is not None]).mean()
        log_data_to_neptune(model_class, expl_loss, 'expl', 'loss', 'epoch', split, ret_dict=None, topk=None)

def log_epoch_metrics(model_class, outputs, split):
    logits = torch.cat([x['logits'] for x in outputs])
    targets = torch.cat([x['targets'] for x in outputs])
    preds = calc_preds(logits)

    perf_metrics = get_step_metrics(preds, targets, model_class.perf_metrics)
    perf_metrics = get_epoch_metrics(model_class.perf_metrics)

    log_data_to_neptune(model_class, perf_metrics['acc'], 'acc', 'metric', 'epoch', split, ret_dict=None, topk=None)
    log_data_to_neptune(model_class, perf_metrics['macro_f1'], 'macro_f1', 'metric', 'epoch', split, ret_dict=None, topk=None)
    log_data_to_neptune(model_class, perf_metrics['micro_f1'], 'micro_f1', 'metric', 'epoch', split, ret_dict=None, topk=None)
    if model_class.num_classes == 2:
        log_data_to_neptune(model_class, perf_metrics['binary_f1'], 'binary_f1', 'metric', 'epoch', split, ret_dict=None, topk=None)