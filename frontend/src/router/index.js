import { createRouter, createWebHistory } from "vue-router";

import { useUserStore } from "@/stores/user";
import Home from "@/views/Home.vue";
import Projects from "@/views/Projects.vue";
// Setup
import ProjectSetup from "@/views/ProjectSetup.vue";
import Document from "@/components/project/setup/Document.vue";
import DocumentList from "@/components/project/setup/DocumentList.vue";
import DocumentUpload from "@/components/project/setup/DocumentUpload.vue";

// Login & Logout
import Login from "@/views/Login.vue";
import Logout from "@/views/Logout.vue";

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
    {
      path: "/project/",
      component: ProjectSetup,
      children: [
        {
          path: "doc/",
          component: Document,
          children: [
            {
              path: "upload",
              name: "DocumentUpload",
              component: DocumentUpload,
            },
            {
              path: "list",
              name: "DocumentList",
              component: DocumentList,
            },
          ],
        },
      ],
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
