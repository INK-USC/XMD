<template>
  <el-col>
    <el-menu>
      <el-menu-item @click="() => this.$router.push({ name: 'DocumentList' })">
        <el-icon><Back /></el-icon>
        <span>Back</span>
      </el-menu-item>
      <el-menu-item @click="() => this.$router.push({ name: 'DebugLocal' })">
        <el-icon><Document /></el-icon>
        <span>Local Explanations</span>
      </el-menu-item>
      <el-menu-item @click="() => this.$router.push({ name: 'DebugGlobal' })">
        <el-icon><DocumentCopy /></el-icon>
        <span>Global Explanations</span>
      </el-menu-item>
    </el-menu>
  </el-col>
</template>

<script>
import { Back, Document, DocumentCopy } from "@element-plus/icons-vue";

// side navigation bar in the debug overview page
export default {
  name: "SetupSideBar",
  components: {
    Back,
    Document,
    DocumentCopy,
  },
};
</script>

<style scoped>
.el-menu {
  border-right: none;
}
</style>
