<template>
  <div></div>
</template>

<script>
import { useUserStore } from "@/stores/user";
// logout user
export default {
  name: "LogoutPage",
  setup() {
    const userStore = useUserStore();
    return {
      userStore,
    };
  },
  created() {
    this.userStore.logout();
  },
};
</script>

<style scoped></style>
