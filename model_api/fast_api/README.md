# Table of Contents
- [Table of Contents](#table-of-contents)
- [Steps to run the FAST api](#steps-to-run-the-fast-api)
- [Schema Definition](#schema-definition)
  - [1. Generate Explanations API](#1-generate-explanations-api)
  - [2. Debug Training API](#2-debug-training-api)

   2.1. [Generate Explanations API](#1-generate-explanations-api)

   2.2. [Debug Training API](#2-debug-training-api)

# Steps to run the FAST api

1. Ensure your `hilt-demo` environment is activated
2. Execute `pip install -r rqs.txt`
3. `uvicorn main:app --reload --port=9000`
4. The API is now exposed on port 9000. Swagger interactive API documentation can be
   found [here](http://127.0.0.1:9000/docs)

# Schema Definition

The complete schema definition can be found in [JSON schema file](json_schema.py). And can also be accessed via Swagger
interactive API documentation.

## 1. Generate Explanations API

- Route - `POST /generate/expl`
- Sample body -

```json
{
  "project_id" : 1,
    "from_local" : "False",
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
                "6f465696-7606-40b2-91be-bf0390e7ff9c", 
                "59393b4c-4c42-43cc-89b3-3d17b7741f30"
            ]
        } 
    },
    "pretrained_model_name_or_path": "bert-base-cased"
}
```

---

## 2. Debug Training API

- Route - `POST /debug/training`
- Sample body -

```json
{
  
}
```

---