import { defineStore } from "pinia";

export const useProjectStore = defineStore({
  id: "project",
  state: () => ({
    projectInfo: null,
  }),
  getters: {
    getProjectInfo: (state) => {
      return state.projectInfo;
    },
  },
  actions: {
    setProject(project) {
      this.projectInfo = project;
    },
  },
});
