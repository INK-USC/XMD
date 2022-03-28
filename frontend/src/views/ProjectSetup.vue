<template>
  <div>
    <el-container>
      <el-aside style="border-right: solid 1px #e6e6e6">
        <SetupSideBar />
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import SetupSideBar from "@/components/project/setup/SetupSideBar.vue";

// placeholder for project page
export default {
  name: "ProjectSetupPage",
  components: {
    SetupSideBar,
  },
};
</script>

<style scoped></style>
