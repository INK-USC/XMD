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
  }
};
