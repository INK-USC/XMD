import { defineStore } from "pinia";

import { useProjectStore } from "@/stores/project";
import LabelsApi from "@/utilities/network/label";

export const useLabelStore = defineStore({
  id: "label",
  state: () => ({
    labels: [],
    labelsMap: {},
  }),
  getters: {
    getLabels: (state) => {
      return state.labels;
    },
    getLabelByID: (state) => {
      return (labelID) => {
        if (!labelID || !(labelID in state.labelsMap)) return null;
        return state.labels[state.labelsMap[labelID]];
      };
    },
  },
  actions: {
    fetchLabels() {
      const projectStore = useProjectStore();
      return LabelsApi.list(projectStore.getProjectInfo.id).then((res) => {
        const labelsMap = {};
        for (let index = 0; index < res.results.length; index++) {
          const label = res.results[index];
          labelsMap[label.id] = index;
        }
        this.labels = res.results;
        this.labelsMap = labelsMap;
        return res.results;
      });
    },
    updateLabel(labelData) {
      const projectStore = useProjectStore();
      return LabelsApi.update(projectStore.getProjectInfo.id, labelData);
    },
  },
});
