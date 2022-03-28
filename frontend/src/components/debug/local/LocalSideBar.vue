<template>
  <el-col>
    <el-menu>
      <el-menu-item @click="() => this.$router.push({ name: 'DebugOverview' })">
        <el-icon><Back /></el-icon>
        <span>Back</span>
      </el-menu-item>
    </el-menu>
  </el-col>
</template>

<script>
import { Back } from "@element-plus/icons-vue";
export default {
  name: "LocalSideBar",
  components: {
    Back,
  },
};
</script>

<style scoped>
.el-menu {
  border-right: none;
}
</style>
