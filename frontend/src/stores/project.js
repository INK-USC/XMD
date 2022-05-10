import { defineStore } from "pinia";

import ProjectsApi from "@/utilities/network/project";

export const useProjectStore = defineStore({
  id: "project",
  state: () => ({
    projectInfo: null,
  }),
  getters: {
    getProjectInfo: (state) => {
      return state.projectInfo;
    },
    task: (state) => {
      return state.projectInfo.task;
    },
  },
  actions: {
    setProject(project) {
      this.projectInfo = project;
    },
    exportJSON() {
      return ProjectsApi.exportJSON(this.projectInfo.id);
    },
  },
});
