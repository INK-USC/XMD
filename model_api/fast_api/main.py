import json
import os
import sys
import requests
import torch
from fastapi import FastAPI, BackgroundTasks
from fastapi import status

import fast_api_util_functions as util_f
import json_schema as schema

sys.path.append('../../hitl-expl-reg/')
# print(sys.path)
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification, AutoConfig
from src.model import lm as lm

app = FastAPI()


@app.get("/test")
async def root():
    """
    Endpoint for testing FastAPI
    """
    return {"message": "Hello World"}


@app.post("/training/captum", status_code=status.HTTP_201_CREATED)
async def start_captum_training(captum_training_payload: schema.CaptumTrainingPayload, background_tasks: BackgroundTasks):
    """
        Endpoint hit by XMD tool's django api to initiate captum process

        input params: # dataset_path, pretrained_model_name_or_path, from_local

        output params:
        
    """
    from_local = captum_training_payload.from_local
    dataset = captum_training_payload.dataset
    pretrained_model_name_or_path = captum_training_payload.pretrained_model_name_or_path

    print(from_local, dataset, pretrained_model_name_or_path)

    # tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path)
    # model = AutoModelForSequenceClassification.from_pretrained(pretrained_model_name_or_path)  
    config = AutoConfig.from_pretrained(pretrained_model_name_or_path)

    # print(model, tokenizer)


    ### extract data from payload schema
    # params = lean_life_payload.params
    # lean_life_data = lean_life_payload.lean_life_data

    ### call function and add task to background
    background_tasks.add_task(captum_call, config, dataset, pretrained_model_name_or_path)


async def captum_call(config, dataset, pretrained_model_name_or_path):
    """
    Captum API call to get attribution scores
    """

    # language_model = lm.LanguageModel( # add params
    #     arch = pretrained_model_name_or_path
    #     dataset = None
    #     optimizer = 
    #     num_classes = config.type_vocab_size
    #     scheduler = 
    #     attr_algo = 'integrated-gradients'
    # )
    # print(language_model)



    # # attrs = language_model.attr_forward() #(input_ids, attn_mask) 

    # return attrs

### make periodic post requests to django to update status of captum