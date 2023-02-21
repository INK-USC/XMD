import json
import os
import sys
import requests
import torch
from fastapi import FastAPI, BackgroundTasks
from fastapi import status

import fast_api_util_functions as util_f
import json_schema as schema


app = FastAPI()


@app.get("/test")
async def root():
    """
    Endpoint for testing FastAPI
    """
    return {"message": "Hello World"}


@app.post("training/captum", status_code=status.HTTP_201_CREATED)
async def start_captum_training(captum_training_payload: schema.CaptumTrainingPayload, background_tasks: BackgroundTasks):
    """
        Endpoint hit by XMD tool's django api to initiate captum process

        input params:

        output params:
        
    """

    ### extract data from payload schema
    # params = lean_life_payload.params
    # lean_life_data = lean_life_payload.lean_life_data

    ### call function and add task to background
    # background_tasks.add_task(train_next_framework_lean_life, params.__dict__, label_space, unlabeled_docs,
    #                           explanation_triples, ner_label_space)


async def captum_call():
    """
    Captum API call to get attribution scores
    """
    response = await requests.get()
    data = response.text

    return data

### make periodic post requests to django to update status of captum