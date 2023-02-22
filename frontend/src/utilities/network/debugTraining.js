import api from "./index";

export default {
  train(projectID) {
    return api.post(
      `hilt/projects/${projectID}/debug/training/`, {
        headers: {
          ...api.defaults.headers,
        },
      }
    );
  },
  didFinishGeneration(projectID) {
    return api.get(`hilt/projects/${projectID}/update/training_debug_model_status/`)
  },
};
