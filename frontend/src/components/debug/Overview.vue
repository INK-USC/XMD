<template>Debug Overview Page

<el-button
      type="primary"
      @click="trainDebugModel()">
      Submit
</el-button>
</template>


<script>
import { useProjectStore } from "@/stores/project";
import DebugTrainingAPI from "@/utilities/network/debugTraining"

export default {
  name: "DebugOverview",
  setup() {
    const projectStore = useProjectStore();
    return {
      projectStore,
    };
  },
  methods: {
    trainDebugModel() {
      DebugTrainingAPI.train(this.projectStore.getProjectInfo.id)
    },
  }
};
</script>
