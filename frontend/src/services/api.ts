// src/services/api.ts
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000", // or wherever your backend runs
});

// Optional: you can intercept requests to add auth tokens
// api.interceptors.request.use((config) => {
//   const token = localStorage.getItem("token");
//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`;
//   }
//   return config;
// });

export default api;
