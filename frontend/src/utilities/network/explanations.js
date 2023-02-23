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
  didFinishGeneration(projectID) {
    return api.get(`hilt/projects/${projectID}/update/model_status/`)
  },
  getAttributeScoresForDoc(projectID, text, label, model_id) {
    console.log('inside network/getAttributeScoresForDoc function')
    const formData = new FormData();
    formData.append("text", text)
        formData.append("label", label)
    formData.append("model_id", model_id)
    console.log(formData)
    return api.post(`hilt/projects/${projectID}/explanations/single`, formData, {
      headers: {
        ...api.defaults.headers,
        "Content-Type": "multipart/form-data",
      },
    });
  }
};
