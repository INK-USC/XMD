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
    reset_state() {
      ProjectsApi.get(this.projectInfo.id).then(
        (res) => {
          console.log('reset_project_state', res)
          this.projectInfo = res;
          return res
        },
        (err) => {
          console.log(err);
        }
      );
    },
    setProject(project) {
      this.projectInfo = project;
    },
    setTask(task) {
      this.projectInfo.task = task;
    },
    exportJSON() {
      return ProjectsApi.exportJSON(this.projectInfo.id);
    },
  },
});
