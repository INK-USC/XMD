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
      params: queryData,
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
  markAnnotated(projectID, docID) {
    console.log('documents API', projectID, ':\t', docID)
    return api.put(`hilt/projects/${projectID}/docs/${docID}/`, {
      annotated: true
    });
  },
  delete(projectID, docID) {
    return api.delete(`hilt/projects/${projectID}/docs/${docID}/`);
  },
  detailedDocument(projectID, docID) {
    return api.get(
      `hilt/projects/${projectID}/docs/${docID}/words-annotations/`
    );
  },
};
