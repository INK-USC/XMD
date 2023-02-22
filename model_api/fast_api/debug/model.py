from transformers import PreTrainedModel
from typing import Optional, Tuple, Union
from transformers.modeling_outputs import SequenceClassifierOutput
from debug.loss import calc_pos_expl_loss
import torch

class DebugModel(PreTrainedModel):
    def __init__(self, classification_model, config):
        super(DebugModel, self).__init__(config)
        self.classification_model = classification_model

    def forward(
        self,
        input_ids: Optional[torch.Tensor] = None,
        attention_mask: Optional[torch.Tensor] = None,
        token_type_ids: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.Tensor] = None,
        head_mask: Optional[torch.Tensor] = None,
        inputs_embeds: Optional[torch.Tensor] = None,
        labels: Optional[torch.Tensor] = None,
        before_reg_rationale: Optional[torch.Tensor] = None,
        after_reg_rationale: Optional[torch.Tensor] = None,
        has_rationale: Optional[torch.Tensor] = None,
    ) -> Union[Tuple[torch.Tensor], SequenceClassifierOutput]:

        output = self.classification_model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
            position_ids=position_ids,
            head_mask=head_mask,
            inputs_embeds=inputs_embeds,
            labels=labels,
            return_dict=True
        )

        task_loss = output.loss
        explanation_loss = calc_pos_expl_loss(
                                attrs=before_reg_rationale,
                                rationale=after_reg_rationale,
                                attn_mask=attention_mask,
                                criterion='mse',
                                has_rationale=has_rationale,
                            )

        loss = task_loss + explanation_loss
        print(task_loss, explanation_loss, loss)

        return SequenceClassifierOutput(
            loss=loss,
            logits=output.logits,
            hidden_states=output.hidden_states,
            attentions=output.attentions,
        )

