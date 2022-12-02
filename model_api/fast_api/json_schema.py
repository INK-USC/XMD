"""
    File the contains input and output data schemas for Fast Api Calls
"""
from pydantic import BaseModel
from typing import Any, List, Dict, Tuple, Union, Optional
from typing_extensions import Literal

class DocMetaData(BaseModel):
    document_ids: List[str]

    class Config:
        schema_extra = {
            "example" : {
                "document_ids": [
                        '6f465696-7606-40b2-91be-bf0390e7ff9c', 
                        '59393b4c-4c42-43cc-89b3-3d17b7741f30'
                ]
            }
        }

class HiltData(BaseModel):
    text: List[str]
    labels: List[int]
    metadata: DocMetaData

    class Config:
        schema_extra = {
            "example": {
                "text": [
                    "There is a big difference between muslims and terrorists",
                    "All muslims are terrorists and need to be deported from this country"
                ],
                "labels": [
                    1,
                    2
                ],
                "metadata": {
                    "document_ids": [
                        '6f465696-7606-40b2-91be-bf0390e7ff9c', 
                        '59393b4c-4c42-43cc-89b3-3d17b7741f30'
                    ]
                } 
            }
        }
class ExplanationGenerationPayload(BaseModel):
    project_id: int
    from_local : bool
    dataset: HiltData
    pretrained_model_name_or_path: str

    class Config:
        schema_extra = {
            "example": {
                "project_id" : 1,
                "from_local" : False,
                "dataset": {
                    "text": [
                        "There is a big difference between muslims and terrorists",
                        "All muslims are terrorists and need to be deported from this country"
                    ],
                    "labels": [
                        1,
                        2
                    ],
                    "metadata": {
                        "document_ids": [
                            '6f465696-7606-40b2-91be-bf0390e7ff9c', 
                            '59393b4c-4c42-43cc-89b3-3d17b7741f30'
                        ]
                    } 
                },
                "pretrained_model_name_or_path": "bert-base-cased"
            }
        }

class TrainDebugPayload(BaseModel):
    pass

    class Config:
        schema_extra = {
            "example": {}
        }