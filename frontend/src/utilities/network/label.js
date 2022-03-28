import api from "./index";

export default {
  list(projectID) {
    return api.get(`hilt/projects/${projectID}/labels/?page_size=100`);
  },
  update(projectID, label) {
    return api.put(`hilt/projects/${projectID}/labels/${label.id}/`, label);
  },
};
