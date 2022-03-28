import api from "./index";

export default {
  list(projectID, pageNum, pageSize) {
    const queryData = {};
    if (pageNum) {
      queryData["page"] = pageNum;
    }
    if (pageSize) {
      queryData["page_size"] = pageSize;
    }
    return api.get(`hilt/projects/${projectID}/docs/`, {
      data: queryData,
    });
  },
  uploadFile(projectID, file, format) {
    const formData = new FormData();
    formData.append("dataset", file);
    formData.append("format", format.toLowerCase());
    return api.post(`hilt/projects/${projectID}/docs/upload/`, formData, {
      headers: {
        ...api.defaults.headers,
        "Content-Type": "multipart/form-data",
      },
    });
  },
};
