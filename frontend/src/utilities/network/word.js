import api from "./index";

export default {
  list(projectID, pageNum, pageSize, query) {
    const queryData = {};
    if (pageNum) {
      queryData["page"] = pageNum;
    }
    if (pageSize !== undefined && pageSize !== null) {
      queryData["page_size"] = pageSize;
    }
    if (query !== undefined && query !== null) {
      queryData["q"] = query;
    }
    return api.get(`hilt/projects/${projectID}/words/`, {
      params: queryData,
    });
  },
  documents(projectID, word) {
    return api.get(`hilt/projects/${projectID}/words/${word}/`);
  },
};
