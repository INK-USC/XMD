<template>
  <el-button type="primary" @click="exportJSON()">
    <el-icon><Download /></el-icon> Download JSON data
  </el-button>
</template>

<script>
import { Download } from "@element-plus/icons-vue";
import { useProjectStore } from "@/stores/project";
import fileDownload from "js-file-download";

export default {
  name: "ExportData",
  components: {
    Download,
  },
  setup() {
    const projectStore = useProjectStore();
    return {
      projectStore,
    };
  },
  methods: {
    exportJSON() {
      this.projectStore.exportJSON().then((res) => {
        fileDownload(
          JSON.stringify(res, null, 1),
          `${this.projectStore.getProjectInfo.name}.json`
        );
      });
      // window.open(, "_blank");
    },
  },
};
</script>
