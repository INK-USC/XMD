<template>
  <h3>Export Explanation-Generated Data
    <el-popover content="help text" trigger="hover" :width="400">
      <template #reference>
        <el-icon style="height: 100%; margin-left: 0.5rem">
          <QuestionFilled />
        </el-icon>
      </template>
    </el-popover>
  </h3>
  <el-button type="primary" @click="exportJSON()">
    <el-icon><Download /></el-icon> Download JSON data
  </el-button>
</template>

<script>
import { Download, QuestionFilled } from "@element-plus/icons-vue";
import { useProjectStore } from "@/stores/project";
import fileDownload from "js-file-download";

export default {
  name: "ExportData",
  components: {
    Download,
    QuestionFilled
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
