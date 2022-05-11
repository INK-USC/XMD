import api from "./index";

export default {
  list(projectID, query) {
    const queryQP = query !== undefined ? `&q=${query}` : "";
    return api.get(
      `hilt/projects/${projectID}/dict/global/?page_size=10000` + queryQP
    );
  },
  create(projectID, data) {
    return api.post(`hilt/projects/${projectID}/dict/global/`, data);
  },
  update(projectID, data) {
    return api.put(`hilt/projects/${projectID}/dict/global/${data.id}/`, data);
  },
  delete(projectID, dictID) {
    return api.delete(`hilt/projects/${projectID}/dict/global/${dictID}/`);
  },
};
