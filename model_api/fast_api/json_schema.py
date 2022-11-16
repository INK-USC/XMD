"""
    File the contains input and output data schemas for Fast Api Calls
"""
from pydantic import BaseModel
from typing import Any, List, Dict, Tuple, Union, Optional
from typing_extensions import Literal

class HiltData(BaseModel):
    text: List[str]
    labels: List[int]

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
                ]
            }
        }
class CaptumTrainingPayload(BaseModel):
    from_local : bool
    dataset: HiltData
    pretrained_model_name_or_path: str

    class Config:
        schema_extra = {
            "example": {
                "from_local" : False,
                "dataset": {
                    "text": [
                        "There is a big difference between muslims and terrorists",
                        "All muslims are terrorists and need to be deported from this country"
                    ],
                    "labels": [
                        1,
                        2
                    ]
                },
                "pretrained_model_name_or_path": "bert-base-cased"
            }
        }

