/**
 * services/api.js
 * ------------------
 * Central axios instance. The Vite dev server proxies /api to the Flask
 * backend (see vite.config.js), so no absolute URL is needed here.
 *
 * Dependencies: axios
 */
import axios from "axios";

const api = axios.create({ baseURL: "/api" });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("aavanam_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("aavanam_token");
      localStorage.removeItem("aavanam_user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
