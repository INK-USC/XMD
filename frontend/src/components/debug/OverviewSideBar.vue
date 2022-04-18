<template>
  <el-col>
    <el-menu :default-active="$route.path">
      <el-menu-item
        index="1"
        @click="() => this.$router.push({ name: 'DocumentList' })"
      >
        <el-icon><Back /></el-icon>
        <span>Back</span>
      </el-menu-item>
      <el-menu-item
        index="/debug/overview"
        @click="() => this.$router.push({ name: 'DebugOverview' })"
      >
        <el-icon><Management /></el-icon>
        <span>Overview</span>
      </el-menu-item>
      <!-- <el-menu-item
        index="/debug/dictionary"
        @click="() => this.$router.push({ name: 'DebugDictionary' })"
      >
        <el-icon><List /></el-icon>
        <span>Dictionary</span>
      </el-menu-item> -->
      <el-menu-item
        index="2"
        @click="() => this.$router.push({ name: 'DebugLocal' })"
      >
        <el-icon><Document /></el-icon>
        <span>Local Explanations</span>
      </el-menu-item>
      <el-menu-item
        index="3"
        @click="() => this.$router.push({ name: 'DebugGlobal' })"
      >
        <el-icon><DocumentCopy /></el-icon>
        <span>Global Explanations</span>
      </el-menu-item>
    </el-menu>
  </el-col>
</template>

<script>
import {
  Back,
  Document,
  DocumentCopy,
  // List,
  Management,
} from "@element-plus/icons-vue";

// side navigation bar in the debug overview page
export default {
  name: "SetupSideBar",
  components: {
    Back,
    Document,
    DocumentCopy,
    // List,
    Management,
  },
};
</script>

<style scoped>
.el-menu {
  border-right: none;
}
</style>
