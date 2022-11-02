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
  }
};
