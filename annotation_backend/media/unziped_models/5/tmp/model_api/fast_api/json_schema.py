"""
    File the contains input and output data schemas for Fast Api Calls
"""
from pydantic import BaseModel
from typing import Any, List, Dict, Tuple, Union, Optional
from typing_extensions import Literal

class CaptumTrainingPayload(BaseModel):
    save_path : str

    class Config:
        schema_extra = {
            "examples": {
                "save_path": ""
            }
        }

