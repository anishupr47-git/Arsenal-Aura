const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function apiFetch(path, options = {}, accessToken) {
  const headers = options.headers || {};
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
    credentials: "include"
  });
  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json") ? await response.json() : null;
  if (!response.ok) {
    let detail = data?.detail || "Request failed.";
    if (!data?.detail && data && typeof data === "object") {
      const firstKey = Object.keys(data)[0];
      if (firstKey) {
        const value = data[firstKey];
        const msg = Array.isArray(value) ? value[0] : value;
        detail = `${firstKey}: ${msg}`;
      }
    }
    throw new Error(detail);
  }
  return data;
}
