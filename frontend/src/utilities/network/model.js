import api from "./index";

export default {
  list(projectID) {
    return api.get(`hilt/projects/${projectID}/models/`);
  },  
  uploadModel(projectID, file, format) {
    const formData = new FormData();
    formData.append("model_zip", file);
    formData.append("format", format.toLowerCase());
    console.log(formData)
    return api.post(`hilt/projects/${projectID}/models/upload/`, formData, {
      headers: {
        ...api.defaults.headers,
        "Content-Type": "multipart/form-data",
      },
    });
  },
  downloadModel(projectID, model_id) {
    const formData = new FormData();
    formData.append("model_id", model_id);
    return api.post(`hilt/projects/${projectID}/model/download/`, formData, {
      headers: {
        ...api.defaults.headers,
        "Content-Type": "multipart/form-data",
      },
      responseType: 'arraybuffer',
    });
  }
};
