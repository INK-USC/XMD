import api from "./index";
import { useUserStore } from "@/stores/user";

export default {
  updateToken(token) {
    api.defaults.headers["Authorization"] = `Bearer ${token}`;
  },
  login(username, password, rememberMe = false) {
    const userStore = useUserStore();
    return api
      .post("token/", {
        username,
        password,
        rememberMe,
      })
      .then((res) => {
        res.token = res.access;
        delete res.access;
        userStore.login({
          ...res,
          username,
        });
        return res;
      });
  },
  refreshToken() {
    const userStore = useUserStore();
    return api
      .post("token/refresh/", { token: userStore.token })
      .then((res) => {
        userStore.updateToken(res.token);
      });
  },
};
