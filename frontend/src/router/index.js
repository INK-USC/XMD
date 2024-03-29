import { createRouter, createWebHistory } from "vue-router";

import { useUserStore } from "@/stores/user";
import Home from "@/views/Home.vue";
import Projects from "@/views/Projects.vue";
// Setup
import ProjectSetup from "@/views/ProjectSetup.vue";
import Document from "@/components/project/setup/Document.vue";
import DocumentList from "@/components/project/setup/DocumentList.vue";
import DocumentUpload from "@/components/project/setup/DocumentUpload.vue";
import ModelUpload from "@/components/project/setup/ModelUpload.vue"
import LabelModification from "@/components/project/setup/LabelModification.vue";
import GenerateExplanations from "@/components/project/setup/GenerateExplanations.vue";
import ExportData from "@/components/project/setup/ExportData.vue";

// Debug
import Debug from "@/views/Debug.vue";
import DebugOverview from "@/components/debug/Overview.vue";
import DebugLocal from "@/components/debug/local/LocalExplanation.vue";
import DebugGlobal from "@/components/debug/global/GlobalExplanation.vue";
import DebugDictionary from "@/components/debug/Dictionary.vue";
import DebugEvaluation from "@/components/debug/Evaluation.vue";

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
            {
              path: "model",
              name: "ModelUpload",
              component: ModelUpload,
            }
          ],
        },
        {
          path: "labels",
          name: "Labels",
          component: LabelModification,
        },
        {
          path: "generate-explanations",
          name: "GenerateExplanations",
          component: GenerateExplanations,
        },
        {
          path: "export",
          name: "ExportData",
          component: ExportData,
        },
      ],
    },
    {
      path: "/debug/",
      component: Debug,
      children: [
        {
          path: "overview",
          name: "DebugOverview",
          component: DebugOverview,
        },
        {
          path: "dictionary",
          name: "DebugDictionary",
          component: DebugDictionary,
        },
        {
          path: "local",
          name: "DebugLocal",
          component: DebugLocal,
        },
        {
          path: "global",
          name: "DebugGlobal",
          component: DebugGlobal,
        },
        {
          path: "evaluation",
          name: "DebugEvaluation",
          component: DebugEvaluation,
        },
      ],
    },
  ],
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  if (!userStore.isLoggedIn && to.name !== "Login" && to.name !== "Home") {
    next("/");
  } else if (to.name == "Login") {
    next();
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
