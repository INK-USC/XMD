<template>
  <el-col>
    <el-menu :default-active="$route.path" :router="true">
      <el-sub-menu index="1">
        <template #title>
          <el-icon>
            <MessageBox />
          </el-icon>
          <span>Corpus</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="/project/doc/list">
            <el-icon><Files /></el-icon>
            Overview
          </el-menu-item>
          <el-menu-item index="/project/doc/upload" :disabled="disabled">
            <el-icon><UploadFilled /></el-icon>
            Upload New Document
          </el-menu-item>
          <!-- <el-menu-item index="/project/doc/model" :disabled="disabled">
            <el-icon><UploadFilled /></el-icon>
            Upload Custom Model
          </el-menu-item> -->
        </el-menu-item-group>
      </el-sub-menu>

      <el-sub-menu index="2">
        <template #title>
          <el-icon>
            <Tools />
          </el-icon>
          <span>Model</span>
        </template>
        <el-menu-item-group>
          <el-menu-item index="/project/doc/model" :disabled="disabled">
            <el-icon><UploadFilled /></el-icon>
            Upload Custom Model
          </el-menu-item>
        </el-menu-item-group>
      </el-sub-menu>

      <el-menu-item index="/project/labels">
        <el-icon><StarFilled /></el-icon>
        <span>Labels</span>
      </el-menu-item>
      <el-menu-item index="/project/generate-explanations">
        <el-icon><DataAnalysis /></el-icon>
        <span>Generate Explanations</span>
      </el-menu-item>
      <!-- <el-menu-item index="/project/export">
        <el-icon><Download /></el-icon>
        <span>Export Data</span>
      </el-menu-item> -->
    </el-menu>
    <el-menu>
      <el-menu-item @click="() => this.$router.push({ name: 'DebugOverview' })">
        <el-icon><Edit /></el-icon>
        <span>Debug</span>
      </el-menu-item>
    </el-menu>
    <el-menu :default-active="$route.path" :router="true">
      <el-menu-item index="/project/export">
        <el-icon><Download /></el-icon>
        <span>Export Data</span>
      </el-menu-item>
    </el-menu>
  </el-col>
</template>

<script>
import {
  Files,
  UploadFilled,
  MessageBox,
  StarFilled,
  Edit,
  Download,
  DataAnalysis,
  Tools,
} from "@element-plus/icons-vue";
import { useProjectStore } from "@/stores/project";

// side navigation bar in the project over view page
export default {
  name: "SetupSideBar",
  components: {
    Files,
    UploadFilled,
    MessageBox,
    StarFilled,
    Edit,
    Download,
    DataAnalysis,
    Tools,
  },
  computed: {
    disabled() {
      const project = this.projectStore.getProjectInfo
      return false
      // return Boolean(project.explanations_status=='running')
    }

  },
  setup() {
    const projectStore = useProjectStore();
    return {
      projectStore,
    };
  },
};
</script>

<style scoped>
.el-menu {
  border-right: none;
}
</style>
