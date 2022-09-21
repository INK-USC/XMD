import numpy as np
import torch
import torch.nn.functional as F
import torchmetrics
from sklearn.metrics import precision_recall_curve, auc, f1_score, average_precision_score


def init_best_metrics():
    return {
        'best_epoch': 0,
        'dev_best_perf': None,
        'test_best_perf': None,
        'dev_best_loss':None,
    }

def init_perf_metrics(num_classes):
    perf_metrics = torch.nn.ModuleDict({
        'acc': torchmetrics.Accuracy(),
        'macro_f1': torchmetrics.F1Score(num_classes=num_classes, average='macro'),
        'micro_f1': torchmetrics.F1Score(num_classes=num_classes, average='micro'),
    })

    assert num_classes >= 2
    if num_classes == 2:
        perf_metrics['binary_f1'] = torchmetrics.F1(num_classes=num_classes, average='micro', ignore_index=0)
    
    return perf_metrics

def calc_preds(logits):
    return torch.argmax(logits, dim=1)

def get_step_metrics(preds, targets, metrics):
    res = {}
    for key, metric_fn in metrics.items():
        res.update({key: metric_fn(preds, targets) * 100})
    return res

def get_epoch_metrics(metrics):
    res = {}
    for key, metric_fn in metrics.items():
        res.update({key: metric_fn.compute() * 100})
        metric_fn.reset()
    return res