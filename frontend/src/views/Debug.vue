<template>
  <div>
    <el-container>
      <el-aside style="border-right: solid 1px #e6e6e6">
        <OverviewSideBar
          style="width: 100%"
          v-if="
            this.$route.path.endsWith('/overview') ||
            this.$route.path.endsWith('/dictionary') ||
            this.$route.path.endsWith('/evaluation')
          "
        />
        <LocalSideBar
          style="width: 100%"
          v-if="this.$route.path.endsWith('/local')"
        />
        <GlobalSideBar
          style="width: 100%"
          v-if="this.$route.path.endsWith('/global')"
        />
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import OverviewSideBar from "@/components/debug/OverviewSideBar.vue";
import LocalSideBar from "@/components/debug/local/LocalSideBar.vue";
import GlobalSideBar from "@/components/debug//global/GlobalSideBar.vue";

export default {
  name: "DebugPage",
  components: {
    OverviewSideBar,
    LocalSideBar,
    GlobalSideBar,
  },
};
</script>
