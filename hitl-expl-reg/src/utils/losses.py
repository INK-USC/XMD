import torch
import torch.nn.functional as F
import numpy as np

DIST_CRITERION_DICT={
    'mse': F.mse_loss,
    'l1': F.l1_loss,
    'huber': F.smooth_l1_loss,
}

def calc_task_loss(logits, targets, reduction='mean', class_weights=None):
    assert len(logits) == len(targets)
    return F.cross_entropy(logits, targets, weight=class_weights, reduction=reduction)

def calc_pos_expl_loss(attrs, rationale, attn_mask, criterion, margin=None, has_rationale=None, attr_scaling=1):
    attrs = attr_scaling * attrs
    assert criterion in ['bce', 'margin', 'mse', 'l1', 'huber', 'order', 'gate']
    max_length = attn_mask.shape[1]
    has_rationale_ = has_rationale.unsqueeze(1).repeat(1, max_length) * attn_mask
    rationale = rationale * has_rationale_
    with torch.no_grad():
        rationale = torch.mul(attrs, rationale)

    num_tokens = has_rationale_.sum()
    if criterion == 'bce':
        assert has_rationale is not None
        pos_wt = (num_tokens - rationale.sum()) / rationale.sum()
        loss = (F.binary_cross_entropy_with_logits(attrs, rationale, pos_weight=pos_wt, reduction='none') * has_rationale_).sum()
        if num_tokens > 0:
            loss /= num_tokens
        else:
            assert loss == 0
        assert not torch.any(torch.isnan(loss))
    elif criterion == 'margin':
        raise NotImplementedError
        margins = attn_mask * margin
        inv_rationale = (1 - rationale) * attn_mask
        loss = (-rationale + inv_rationale) * attrs
        assert not torch.any(torch.isnan(loss))
        loss = torch.maximum(-margins, loss) + margins
        loss = torch.sum(loss) / torch.sum(attn_mask)
    elif criterion == 'mse' or criterion == 'l1' or criterion == 'huber':
        attrs = F.sigmoid(attrs)
        loss = (DIST_CRITERION_DICT[criterion](attrs, rationale, reduction='none') * has_rationale_).sum()
        if num_tokens > 0:
            loss /= num_tokens
        else:
            assert loss == 0
        assert not torch.any(torch.isnan(loss))
    elif criterion == "order":
        attrs = F.sigmoid(attrs)
        max_non_rationale_attr = torch.max((1-rationale)*attrs, dim=1).values.unsqueeze(1).expand(-1, attrs.shape[1])
        ordered_attr = torch.where(rationale==1, torch.sub(torch.div((rationale * attrs), max_non_rationale_attr), torch.tensor(1.0).to(rationale.device)), torch.tensor(0.0).to(rationale.device))
        loss = torch.sum(torch.square(torch.minimum(ordered_attr, torch.zeros(size=ordered_attr.shape).to(rationale.device))), dim=1)
        loss = loss.mean()
        assert not torch.any(torch.isnan(loss))
    elif criterion == "gate":
        raise NotImplementedError
        max_length = attn_mask.shape[1]
        has_rationale_ = has_rationale.unsqueeze(1).repeat(1, max_length) * attn_mask
        rationale = rationale * has_rationale_
        num_tokens = has_rationale_.sum()
        attrs = F.softmax(attrs, dim=1)
        max_non_rationale_attr = torch.max((1-rationale)*attrs, dim=1).values.unsqueeze(1).expand(-1, attrs.shape[1])
        ordered_attr = torch.where(rationale==1, torch.sub(torch.div((rationale * attrs), max_non_rationale_attr), torch.tensor(1.0).to(rationale.device)), torch.tensor(0.0).to(rationale.device))
        order_loss = torch.sum(torch.square(torch.minimum(ordered_attr, torch.zeros(size=ordered_attr.shape).to(rationale.device))), dim=1)
        bern_probability = torch.add(-torch.sum(torch.where(rationale==1, attrs, torch.tensor(0.0).to(rationale.device)), dim=1),torch.tensor(1.0).to(rationale.device))
        gate_loss = torch.bernoulli(bern_probability) * order_loss
        loss = gate_loss.mean()
        assert not torch.any(torch.isnan(loss))
    assert not torch.isnan(loss)
    return loss

def calc_neg_expl_loss(attrs, attn_mask, criterion, targets, preds=None):
    assert criterion in ['l1', 'l1_incorrect']
    batch_size, num_classes, max_length = attrs.shape
    all_classes = torch.arange(num_classes).to(targets.device).unsqueeze(0).expand(batch_size, -1)

    if criterion == 'l1':
        targets_ = targets.unsqueeze(1).expand(-1, num_classes)
        neg_nz = torch.nonzero(all_classes != targets_)
        neg_classes = all_classes[neg_nz[:, 0], neg_nz[:, 1]].reshape(batch_size, -1).unsqueeze(2).expand(-1, -1, max_length)
        neg_attrs = torch.gather(attrs, dim=1, index=neg_classes)

        attn_mask_ = attn_mask.unsqueeze(1).expand(-1, num_classes-1, -1)
        num_tokens = attn_mask_.sum()
        loss = torch.abs(neg_attrs * attn_mask_).sum() / num_tokens

    elif criterion == 'l1_incorrect':
        assert preds is not None

        preds_ = preds.unsqueeze(1).expand(-1, num_classes)
        pred_nz = torch.nonzero(all_classes == preds_)
        pred_classes = all_classes[pred_nz[:, 0], pred_nz[:, 1]].reshape(batch_size, -1).unsqueeze(2).expand(-1, -1, max_length)
        neg_attrs = torch.gather(attrs, dim=1, index=pred_classes).squeeze(1)

        incorrect_mask = (targets != preds).long().unsqueeze(1).expand(-1, max_length) * attn_mask
        num_tokens = incorrect_mask.sum()
        loss = torch.abs(neg_attrs * incorrect_mask).sum()
        if num_tokens != 0:
            loss = loss / num_tokens

    else:
        raise NotImplementedError

    assert not torch.isnan(loss)
    return loss