<template>
  <div id="app">
    <NavBar style="width: 100%" />
    <router-view />
  </div>
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}

.el-dialog__body {
  padding-top: 0;
}
</style>
<script>
import NavBar from "@/components/NavBar.vue";

export default {
  components: { NavBar },
};
</script>
