from typing import Any, List, Sequence
from torch.utils.data import Dataset
from transformers import BatchEncoding, PreTrainedTokenizer

class DebugDataset(Dataset):
  def __init__(
          self,
          data: List[Any],
          tokenizer: PreTrainedTokenizer,
          max_sequence_length: int,
  ):
    self.data = data
    self.features: Sequence[BatchEncoding] = []
    self.tokenizer = tokenizer
    self.max_sequence_length = max_sequence_length
    self.features = self.convert_examples_to_features(
        self.data, tokenizer
    )

  def __len__(self) -> int:
    return len(self.features)

  def __getitem__(self, index):
    input_ids = self.features[index]["input_ids"]
    attention_mask = self.features[index]["attention_mask"]
    before_reg_rationale = self.features[index]["before_reg_rationale"]
    after_local_reg_rationale = self.features[index]["after_local_reg_rationale"]
    after_global_reg_rationale = self.features[index]["after_global_reg_rationale"]
    has_rationale = self.features[index]["has_rationale"]
    labels = self.features[index]["labels"]

    return {
      "input_ids": input_ids,
      "attention_mask": attention_mask,
      "before_reg_rationale": before_reg_rationale,
      "after_local_reg_rationale": after_local_reg_rationale,
      "after_global_reg_rationale": after_global_reg_rationale,
      "has_rationale": has_rationale,
      "labels": labels
    }

  def convert_examples_to_features(
          self,
          examples: List[Any],
          tokenizer: PreTrainedTokenizer,
  ):
    features = []

    # tokens, label, before_expl_reg, local_after_expl_reg, global_after_expl_reg
    for example in examples:
      assert len(example.tokens) == len(example.before_expl_reg) == len(example.local_after_expl_reg) == len(example.global_after_expl_reg)
      input_ids = tokenizer.encode(example.tokens, is_pretokenized=True)
      before_reg_rationale = [float(0)] + [float(x) for x in example.before_expl_reg] + [float(0)]
      after_local_reg_rationale = [float(0)] + [float(x) for x in example.local_after_expl_reg] + [float(0)]
      after_global_reg_rationale = [float(0)] + [float(x) for x in example.global_after_expl_reg] + [float(0)]

      assert len(input_ids) == len(after_local_reg_rationale) == len(after_global_reg_rationale)

      num_tokens = len(input_ids)
      num_pad_tokens = self.max_sequence_length - num_tokens
      assert num_pad_tokens >= 0

      input_ids += [tokenizer.pad_token_id] * num_pad_tokens
      attention_mask = [1] * num_tokens + [0] * num_pad_tokens
      after_local_reg_rationale += [0] * num_pad_tokens
      after_global_reg_rationale += [0] * num_pad_tokens

      before_reg_rationale += [0] * num_pad_tokens
      has_rationale = int(sum(after_local_reg_rationale) > 0)

      features.append(
        {
          "input_ids": input_ids,
          "attention_mask": attention_mask,
          "before_reg_rationale": before_reg_rationale,
          "after_local_reg_rationale": after_local_reg_rationale,
          "after_global_reg_rationale": after_global_reg_rationale,
          "has_rationale": has_rationale,
          "labels": example.label
        }
      )

    return features
