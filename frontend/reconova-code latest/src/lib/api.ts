// // FastAPI base URL — set VITE_API_URL in .env, else defaults to localhost:8000
// export const API_BASE = (import.meta.env.VITE_API_URL as string) || "http://localhost:8000";

// export async function apiRequest<T = unknown>(path: string, opts: RequestInit = {}): Promise<T> {
//   const res = await fetch(`${API_BASE}${path}`, {
//     headers: { "Content-Type": "application/json", ...(opts.headers || {}) },
//     ...opts,
//   });
//   if (!res.ok) throw new Error(await res.text());
//   return res.json() as Promise<T>;
// }

import axios from "axios";

// Fallback chain ensures it points to live Render backend if VITE_API_URL is undefined
const API_URL =
   import.meta.env.VITE_API_URL ||
  "https://reconova-1.onrender.com";

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor: Inject bearer token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
