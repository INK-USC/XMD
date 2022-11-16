import api from "./index";

export default {
  generateExplanations(projectID, useHuggingface, {str, model_id, model_path} = {}) {
    console.log('inside network/explanations.js');
    const formData = new FormData();
    formData.append("useHuggingface", useHuggingface)
    if (useHuggingface) {
        formData.append("str", str)
    } else {
        formData.append("model_id", model_id)
        formData.append("model_path", model_path)
    };
    console.log(formData);
    return api.post(`hilt/projects/${projectID}/explanations/`, formData, {
      headers: {
        ...api.defaults.headers,
        "Content-Type": "multipart/form-data",
      },
    });
  },
};
