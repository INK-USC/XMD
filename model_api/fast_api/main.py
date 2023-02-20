import json
import os
import sys
import warnings
import requests
import time
import torch
from fastapi import FastAPI, BackgroundTasks
from fastapi import status
from fastapi.encoders import jsonable_encoder

import fast_api_util_functions as util_f
import json_schema as schema

from transformers import AutoTokenizer, AutoModel
from transformers import AutoModelForSequenceClassification, AutoConfig
from captum.attr import IntegratedGradients, GradientShap, InputXGradient, Saliency, DeepLift

from config import attr_algos, baseline_required, dataset_info
from fast_api_util_functions import _send_update

app = FastAPI()

baseline_required_dict = {
    'integrated-gradients': True,
    'gradient-shap': True,
    'input-x-gradient': False,
    'saliency': False,
    'deep-lift': True,
}

attr_algos_dict = {
    'integrated-gradients': IntegratedGradients,
    'gradient-shap': GradientShap,
    'input-x-gradient': InputXGradient,
    'saliency': Saliency,
    'deep-lift': DeepLift,
}


@app.post("/generate/expl", status_code=status.HTTP_201_CREATED)
async def start_expl_generation(explanation_generation_payload: schema.ExplanationGenerationPayload, background_tasks: BackgroundTasks):
    """
        Endpoint hit by XMD tool's django api to initiate captum process

        input params: explanation_generation_payload

        output params: None

    """
    project_id = explanation_generation_payload.project_id
    from_local = explanation_generation_payload.from_local
    dataset = explanation_generation_payload.dataset
    pretrained_model_name_or_path = explanation_generation_payload.pretrained_model_name_or_path
    # config = AutoConfig.from_pretrained(pretrained_model_name_or_path)

    print(from_local, dataset, pretrained_model_name_or_path)
    background_tasks.add_task(
        generate_attr_pipeline, project_id, dataset, pretrained_model_name_or_path)


# Generate attributes for Explanation Generation task
def generate_attr_pipeline(project_id, dataset, arch):
    """
    Captum API call to get attribution scores
    """
    start = time.time()
    model = AutoModelForSequenceClassification.from_pretrained(arch)
    config = AutoConfig.from_pretrained(arch)

    num_classes = len(config.label2id)
    attr_algo = 'input-x-gradient'

    if config.model_type == "bert":
        task_encoder = model.bert
    elif config.model_type == "roberta":
        task_encoder = model.roberta

    # TODO: need to add all the model types. (maybe in dictionary format)

    task_head = model.classifier
    tokenizer = AutoTokenizer.from_pretrained(arch)  # Tokenizer Initialize

    text, labels = dataset.text, dataset.labels
    data = tokenizer(text, padding=True)
    input_ids, attention_mask = data['input_ids'], data['attention_mask']
    input_ids = torch.tensor(input_ids)
    attention_mask = torch.tensor(attention_mask)

    batch_size = input_ids.shape[0]
    seq_length = input_ids.shape[1]
    input_ids_ = input_ids.unsqueeze(
        1).expand(-1, num_classes, -1).reshape(-1, seq_length)
    attention_mask_ = attention_mask.unsqueeze(
        1).expand(-1, num_classes, -1).reshape(-1, seq_length)
    all_classes = torch.arange(num_classes).to(
        input_ids.device).unsqueeze(0).expand(batch_size, -1).flatten()
    input_ids, attention_mask = input_ids_, attention_mask_
    targets = all_classes

    word_emb_layer = task_encoder.embeddings.word_embeddings
    input_embeds = word_emb_layer(input_ids)
    baseline_required = baseline_required_dict[attr_algo]
    if baseline_required:
        baseline = torch.full(
            input_ids.shape, tokenizer.pad_token_id, device=input_ids.device).long()
        baseline[:, 0] = tokenizer.cls_token_id
        sep_token_locs = torch.nonzero(input_ids == tokenizer.sep_token_id)
        baseline[sep_token_locs[:, 0],
                 sep_token_locs[:, 1]] = tokenizer.sep_token_id
        baseline_embeds = word_emb_layer(baseline)
    else:
        baseline_embeds = None

    def forward_func(input_embeds, attention_mask):
        enc = task_encoder(inputs_embeds=input_embeds,
                           attention_mask=attention_mask)[0]
        logits = task_head(enc)
        return logits

    attr_func = attr_algos_dict[attr_algo](forward_func)

    if attr_algo in ['input-x-gradient', 'saliency']:
        attrs = attr_func.attribute(
            inputs=input_embeds.requires_grad_(),
            target=targets, additional_forward_args=(attention_mask),
        ).float()

    attrs = torch.sum(attrs, dim=-1)
    attrs = attrs * attention_mask
    assert not torch.any(torch.isnan(attrs))

    attrs.reshape(batch_size, num_classes, seq_length)
    attrs = attrs.detach().cpu().tolist()
    attrs = [["{0:0.2f}".format(attr) for attr in lst] for lst in attrs]
    end = time.time()
    print(f'time elapsed: {end - start}')

    # format attrs
    document_ids = dataset.metadata.document_ids
    format_attrs = []


    manual_labels = {}
    for i, x in enumerate(sorted(list(set(labels)))):
        manual_labels[x] = i
    print(manual_labels)

    for i, arr in enumerate(text):
        if labels[i] in config.label2id:
            format_attrs.append(
                {
                    "id": i,
                    "tokens": text[i].split(" "),
                    "label": labels[i],
                    "prediction": 1,
                    "before_reg_explanation": attrs[2*i + config.label2id[labels[i]] - 1],
                    "document_id": document_ids[i]
                }
            )
        else:
            format_attrs.append(
                {
                    "id": i,
                    "tokens": text[i].split(" "),
                    "label": labels[i],
                    "prediction": 1,
                    "before_reg_explanation": attrs[2*i + manual_labels[labels[i]] - 1],
                    "document_id": document_ids[i]
                }
            )

    return_json = jsonable_encoder(format_attrs)
    print(return_json)

    # send update back to django
    resp = _send_update(project_id, return_json)
    print(resp)

    return resp


@app.post("/debug/training", status_code=status.HTTP_201_CREATED)
async def start_debug_training_phase(train_debug_payload: schema.TrainDebugModelPayload, background_tasks: BackgroundTasks):
    """
        Endpoint hit by XMD tool's django api to initiate training of debugging model

        input params: train_debug_payload

        output params: None

    """
    print(train_debug_payload)
