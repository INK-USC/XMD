import { createApp } from "vue";
import { createPinia } from "pinia";
import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import VueSnip from "vue-snip";

// ElementPlus library
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import locale from "element-plus/es/locale/lang/en";

// code-base imports
import App from "@/App.vue";
import router from "@/router";
import api from "@/utilities/network";

const app = createApp(App);

// general importing, vue settings
app.use(VueSnip);

// attach api for easy access
app.provide("$api", api);

app.use(ElementPlus, { locale });

// state storage
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);
app.use(pinia);

// router
app.use(router);

app.mount("#app");
