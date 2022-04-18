import api from "./index";

export default {
  list(projectID, docID) {
    const docQP = docID !== undefined ? `&doc_id=${docID}` : "";
    return api.get(
      `hilt/projects/${projectID}/dict/local/?page_size=10000` + docQP
    );
  },
  create(projectID, data) {
    return api.post(`hilt/projects/${projectID}/dict/local/`, data);
  },
  delete(projectID, dictID) {
    return api.delete(`hilt/projects/${projectID}/dict/local/${dictID}/`);
  },
};
