import jwt_decode from "jwt-decode";
import { defineStore } from "pinia";
import router from "@/router";

import UserApi from "@/utilities/network/user";

export const useUserStore = defineStore({
  id: "user",
  presist: true,
  state: () => ({
    userInfo: null,
  }),
  getters: {
    username: (state) => {
      return state.userInfo.username;
    },
    token: (state) => {
      return state.userInfo.token;
    },
    isLoggedIn: (state) => {
      return state.userInfo !== null;
    },
  },
  actions: {
    login(loginData) {
      this.userInfo = loginData;
      UserApi.updateToken(loginData.token);
      router.push({ name: "Projects" }).then((r) => r);
    },
    logout() {
      this.userInfo = null;
      router.push("/").then((r) => r);
    },
    updateToken(token) {
      this.userInfo.token = token;
      UserApi.updateToken(token);
    },
    inspectToken() {
      // 1. IF it has expired => DO NOT REFRESH / PROMPT TO RE-OBTAIN TOKEN
      // 2. IF it is expiring in 30 minutes (1800 second) AND it is not reaching its lifespan (7 days — 30 mins = 630000–1800 = 628200) => REFRESH
      // 3. IF it is expiring in 30 minutes AND it is reaching its lifespan => DO NOT REFRESH

      const token = this.userInfo.token;
      if (token) {
        const decoded = jwt_decode(token);
        const exp = decoded.exp;
        const orig_iat = decoded.orig_iat;
        if (exp < Date.now() / 1000) {
          this.logout();
        } else if (
          exp - Date.now() / 1000 < 1800 &&
          Date.now() / 1000 - orig_iat < 628200
        ) {
          UserApi.refreshToken();
        } else if (exp - Date.now() / 1000 < 1800) {
          // DO NOTHING, DO NOT REFRESH
        }
      }
    },
  },
});
