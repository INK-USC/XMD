import axios from "axios";
import { ElNotification } from "element-plus";

// eslint-disable-next-line no-undef
axios.defaults.baseURL = import.meta.env.VITE_API_ENDPOINT;

// preconfigure axios to simplify requests and intercept error to show notification
const api = axios.create({
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
    Authorization: null,
  },
});

api.interceptors.response.use(
  (res) => {
    // Any status code that lie within the range of 2xx cause this function to trigger
    // Do something with response data
    return res.data;
  },
  (err) => {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    ElNotification({
      title: "Error",
      message: err.toString(),
      type: "error",
    });
    return Promise.reject(err);
  }
);

api.interceptors.request.use(
  (config) => {
    return config;
  },
  (err) => {
    ElNotification({
      title: "Error",
      message: err.toString(),
      type: "error",
    });
    return Promise.reject(err);
  }
);

export default api;
