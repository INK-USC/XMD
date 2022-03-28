import { defineStore } from "pinia";

import { useProjectStore } from "@/stores/project";
import LabelsApi from "@/utilities/network/label";

export const useLabelStore = defineStore({
  id: "label",
  state: () => ({
    labels: [],
  }),
  getters: {
    getLabels: (state) => {
      return state.labels;
    },
  },
  actions: {
    fetchLabels() {
      const projectStore = useProjectStore();
      return LabelsApi.list(projectStore.getProjectInfo.id).then((res) => {
        this.labels = res.results;
        return res.results;
      });
    },
    updateLabel(labelData) {
      const projectStore = useProjectStore();
      return LabelsApi.update(projectStore.getProjectInfo.id, labelData);
    },
  },
});
