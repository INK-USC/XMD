import api from "./index";

export default {
  list() {
    return api.get("hilt/projects/");
  },
  get(projectID) {
    return api.get(`hilt/projects/${projectID}/`)
  },
  create(project) {
    return api.post("hilt/projects/", project);
  },
  update(project) {
    return api.put(`hilt/projects/${project.id}/`, project);
  },
  delete(projectID) {
    return api.delete(`hilt/projects/${projectID}/`);
  },
  exportJSON(projectID) {
    return api.get(`hilt/export/json/${projectID}/`);
  },
};
