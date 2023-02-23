import os
import time
import torch
from fastapi import FastAPI, BackgroundTasks
from fastapi import status
from fastapi.encoders import jsonable_encoder

import json_schema as schema

from transformers import (
    AutoConfig,
    AutoModel,
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    HfArgumentParser,
)
from captum.attr import IntegratedGradients, GradientShap, InputXGradient, Saliency, DeepLift
from debug.dataset import DebugDataset
from debug.model import DebugModel
import numpy as np
from fast_api_util_functions import _send_update_generate_explanation, _send_update_debug_model

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
    dataset = explanation_generation_payload.dataset
    pretrained_model_name_or_path = explanation_generation_payload.pretrained_model_name_or_path

    background_tasks.add_task(
        generate_attr_pipeline, project_id, dataset, pretrained_model_name_or_path)

@app.post("/generate/expl/single", status_code=status.HTTP_201_CREATED)
async def start_expl_generation(explanation_generation_payload: schema.ExplanationGenerationSinglePayload):
    """
        Endpoint hit by XMD tool's django api to initiate captum process

        input params: explanation_generation_payload

        output params: None

    """
    # Unload Payload (model, label, text)
    text = explanation_generation_payload.text
    label = explanation_generation_payload.label
    arch = explanation_generation_payload.model_path

    tokenizer = AutoTokenizer.from_pretrained(arch)
    config = AutoConfig.from_pretrained(arch)
    debug_model = DebugModel.from_pretrained(pretrained_model_name_or_path=arch, config=config)
    model = debug_model.classification_model

    original_input_ids, attrs = generate_attr([text], model, tokenizer, config)

    start_index = original_input_ids[0].index(tokenizer.cls_token_id)
    end_index = original_input_ids[0].index(tokenizer.sep_token_id)
    tokens = tokenizer.batch_decode(torch.tensor(original_input_ids[0][start_index + 1:end_index]).unsqueeze(1))

    if label in config.label2id:
        attribution_scores = attrs[config.label2id[label]][start_index + 1:end_index]
    else:
        attribution_scores = attrs[int(label)][start_index + 1:end_index]

    attribution_scores = np.exp(attribution_scores) / np.sum(np.exp(attribution_scores), axis=0)
    attribution_scores = ["{0:0.2f}".format(attr) for attr in attribution_scores]

    format_attrs = {
       'res': [
            {
            'text': tokens,
            'score': attribution_scores
            }
        ]
    }
    return_json = jsonable_encoder(format_attrs)

    # Generate Attribution score
    return return_json

def generate_attr(text, model, tokenizer, config):
    num_classes = len(config.label2id)
    attr_algo = 'input-x-gradient'

    # TODO: need to add all the model types. (maybe in dictionary format)
    if config.model_type == "bert":
        task_encoder = model.bert
    elif config.model_type == "roberta":
        task_encoder = model.roberta

    task_head = model.classifier
    data = tokenizer(text, padding=True)
    input_ids, attention_mask = data['input_ids'], data['attention_mask']
    original_input_ids = input_ids
    input_ids = torch.tensor(input_ids)

    attention_mask = torch.tensor(attention_mask)

    batch_size = input_ids.shape[0]
    seq_length = input_ids.shape[1]
    input_ids_ = input_ids.unsqueeze(1).expand(-1, num_classes, -1).reshape(-1, seq_length)
    attention_mask_ = attention_mask.unsqueeze(1).expand(-1, num_classes, -1).reshape(-1, seq_length)
    all_classes = torch.arange(num_classes).to(input_ids.device).unsqueeze(0).expand(batch_size, -1).flatten()
    input_ids, attention_mask = input_ids_, attention_mask_

    targets = all_classes

    word_emb_layer = task_encoder.embeddings.word_embeddings
    input_embeds = word_emb_layer(input_ids)
    baseline_required = baseline_required_dict[attr_algo]

    if baseline_required:
        baseline = torch.full(input_ids.shape, tokenizer.pad_token_id, device=input_ids.device).long()
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
    attrs = attrs * 100
    attrs = attrs.detach().cpu().tolist()
    return original_input_ids, attrs

# Generate attributes for Explanation Generation task
def generate_attr_pipeline(project_id, dataset, arch):
    """
    Captum API call to get attribution scores
    """
    start = time.time()

    model = AutoModelForSequenceClassification.from_pretrained(arch)
    tokenizer = AutoTokenizer.from_pretrained(arch)
    config = AutoConfig.from_pretrained(arch)
    text, labels = dataset.text, dataset.labels
    original_input_ids, attrs = generate_attr(text, model, tokenizer, config)

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
        start_index = original_input_ids[i].index(tokenizer.cls_token_id)
        end_index = original_input_ids[i].index(tokenizer.sep_token_id)
        tokens = tokenizer.batch_decode(torch.tensor(original_input_ids[i][start_index+1:end_index]).unsqueeze(1))

        if labels[i] in config.label2id:
            attribution_scores = attrs[2*i + config.label2id[labels[i]] - 1][start_index+1:end_index]
        else:
            attribution_scores = attrs[2*i + manual_labels[labels[i]] - 1][start_index+1:end_index]

        attribution_scores = np.exp(attribution_scores) / np.sum(np.exp(attribution_scores), axis=0)
        attribution_scores = ["{0:0.2f}".format(attr) for attr in attribution_scores]

        format_attrs.append(
            {
                "id": i,
                "tokens": tokens,
                "label": labels[i],
                "prediction": 1,
                "before_reg_explanation": attribution_scores,
                "document_id": document_ids[i]
            }
        )

    return_json = jsonable_encoder(format_attrs)
    for x in return_json[:3]:
        print(x)

    # send update back to django
    resp = _send_update_generate_explanation(project_id, return_json)
    print(resp)
    return resp


@app.post("/debug/training", status_code=status.HTTP_201_CREATED)
async def start_debug_training_phase(train_debug_payload: schema.TrainDebugModelPayload, background_tasks: BackgroundTasks):
    """
        Endpoint hit by XMD tool's django api to initiate training of debugging model

        input params: train_debug_payload

        output params: None

    """
    project_id = train_debug_payload.project_id
    dataset = train_debug_payload.dataset
    pretrained_model_name_or_path = train_debug_payload.pretrained_model_name_or_path
    background_tasks.add_task(train_debug_pipeline, project_id, dataset, pretrained_model_name_or_path)

# Debugging pipeline
def train_debug_pipeline(project_id, dataset, arch):
    """
    Captum API call to get attribution scores
    """
    start = time.time()
    tokenizer = AutoTokenizer.from_pretrained(arch)
    config = AutoConfig.from_pretrained(arch)

    debug_model = DebugModel(config=config)
    dataset = DebugDataset(dataset, tokenizer, 128)

    trial_index = 1
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_dir = os.path.join(root_dir, f'annotation_backend/media/debug_models/trial{trial_index}')

    training_args = TrainingArguments(
        output_dir=output_dir
    )

    trainer = Trainer(
        model=debug_model,
        args=training_args,
        train_dataset=dataset,
        eval_dataset=dataset,
    )

    trainer.train()
    trainer.save_model()
    tokenizer.save_pretrained(output_dir)

    format_attrs = {"save_model_path": output_dir}
    return_json = jsonable_encoder(format_attrs)
    resp = _send_update_debug_model(project_id, return_json)

    end = time.time()
    print(f'time elapsed: {end - start}')
    
    return resp


