from transformers import AutoModelForSequenceClassification, PreTrainedModel
from typing import Optional, Tuple, Union
from transformers.modeling_outputs import SequenceClassifierOutput
from debug.loss import calc_pos_expl_loss
import torch

class DebugModel(PreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.classification_model = AutoModelForSequenceClassification.from_config(config)
        self.config = config

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
        after_local_reg_rationale: Optional[torch.Tensor] = None,
        after_global_reg_rationale: Optional[torch.Tensor] = None,
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
        local_explanation_loss = calc_pos_expl_loss(
                                attrs=before_reg_rationale,
                                rationale=after_local_reg_rationale,
                                attn_mask=attention_mask,
                                criterion='mse',
                                has_rationale=has_rationale,
                            )
        global_explanation_loss = calc_pos_expl_loss(
                                attrs=before_reg_rationale,
                                rationale=after_global_reg_rationale,
                                attn_mask=attention_mask,
                                criterion='mse',
                                has_rationale=has_rationale,
                            )
        loss = task_loss + local_explanation_loss + global_explanation_loss
        print(f"total loss: {loss} / task loss: {task_loss} / local explanation loss: {local_explanation_loss} / global explanation loss: {global_explanation_loss}")

        return SequenceClassifierOutput(
            loss=loss,
            logits=output.logits,
            hidden_states=output.hidden_states,
            attentions=output.attentions,
        )

