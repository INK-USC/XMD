import torch
import torch.nn.functional as F

DIST_CRITERION_DICT={
    'mse': F.mse_loss,
    'l1': F.l1_loss,
    'huber': F.smooth_l1_loss,
}

def calc_pos_expl_loss(attrs, rationale, attn_mask, criterion, has_rationale=None, attr_scaling=1):
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

    elif criterion == 'mse' or criterion == 'l1' or criterion == 'huber':
        attrs = F.sigmoid(attrs)
        loss = (DIST_CRITERION_DICT[criterion](attrs, rationale, reduction='none') * has_rationale_).sum()
        if num_tokens > 0:
            loss /= num_tokens
        else:
            assert loss == 0
        assert not torch.any(torch.isnan(loss))

    assert not torch.isnan(loss)
    return loss