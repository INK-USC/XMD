<template>
  <el-menu :default-active="$route.path" mode="horizontal" :router="true">
    <el-menu-item index="/">
      <el-image :src="Logo" style="width: 58px; height: 58px" />
    </el-menu-item>
<!--    <el-menu-item index="1">-->
<!--      &lt;!&ndash; <a href="http://inklab.usc.edu/" class="el-link" target="_blank">HILT</a> &ndash;&gt;-->
<!--      HILT-->
<!--    </el-menu-item>-->
    <el-menu-item index="/projects" v-if="userStore.isLoggedIn">
      Projects
    </el-menu-item>
    <!-- <el-menu-item index="/models" v-if="userStore.isLoggedIn"> Models </el-menu-item> -->

    <el-menu-item
      :index="!userStore.isLoggedIn ? '/login' : '/logout'"
      class="dock-right"
    >
      <el-button @click="loginClicked($event)" jest="logBtn">
        {{ !this.userStore.isLoggedIn ? "Login" : "Logout" }}
      </el-button>
    </el-menu-item>
  </el-menu>
</template>

<script>
import { useUserStore } from "@/stores/user";
import Logo from "@/assets/logo.png";

// nav bar
export default {
  name: "NavBar",
  components: {},
  setup() {
    const userStore = useUserStore();
    return {
      userStore,
      Logo,
    };
  },
  methods: {
    loginClicked() {
      if (this.userStore.isLoggedIn) {
        this.$router.push("/login");
      } else {
        this.$router.push("/logout");
      }
    },
  },
};
</script>

<style scoped>
.el-menu {
  display: block;
}

.el-menu > .el-menu-item.dock-right {
  float: right;
}
</style>
