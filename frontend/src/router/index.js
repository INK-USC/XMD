import { createRouter, createWebHistory } from "vue-router";

import { useUserStore } from "@/stores/user";
import Home from "@/views/Home.vue";
import Projects from "@/views/Projects.vue";
import Login from "@/components/Login.vue";
import Logout from "@/components/Logout.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home,
    },
    {
      path: "/projects",
      name: "Projects",
      component: Projects,
    },
    {
      path: "/login",
      name: "Login",
      component: Login,
    },
    {
      path: "/logout",
      component: Logout,
    },
  ],
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  if (!userStore.isLoggedIn && to.name !== "Login" && to.name !== "Home") {
    next("/login");
  } else {
    next();
  }
});

router.afterEach(() => {
  const userStore = useUserStore();
  if (userStore.isLoggedIn) {
    userStore.inspectToken();
  }
});

export default router;
