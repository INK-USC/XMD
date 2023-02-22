"""
    Utility Functions used by Fast API to prepare data and send requests back to XMD tool's frontend
"""

import requests
import fast_api_constants as const

def _send_update_generate_explanation(project_id, data):
    end_point = const.HILT_URL + f"projects/{project_id}/update/generate_expl_metadata/"
    params = {
        'project_id': project_id,
    }
    response = requests.post(end_point, json=data, params=params)
    return response.status_code

def _send_update_debug_model(project_id, data):
    end_point = const.HILT_URL + f"projects/{project_id}/update/training_debug_model_metadata/"
    params = {
        'project_id': project_id,
    }
    response = requests.post(end_point, json=data, params=params)
    return response.status_code