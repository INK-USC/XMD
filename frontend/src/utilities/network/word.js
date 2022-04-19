import api from "./index";

export default {
  list(projectID, pageNum, pageSize) {
    const queryData = {};
    if (pageNum) {
      queryData["page"] = pageNum;
    }
    if (pageSize !== undefined && pageSize !== null) {
      queryData["page_size"] = pageSize;
    }
    return api.get(`hilt/projects/${projectID}/words/`, {
      params: queryData,
    });
  },
  documents(projectID, word) {
    return api.get(`hilt/projects/${projectID}/words/${word}/`);
  },
};
