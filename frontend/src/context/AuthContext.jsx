import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { apiFetch } from "../api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState("");
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadMe = async (token) => {
    const data = await apiFetch("/api/me", { method: "GET" }, token);
    setUser(data);
  };

  const refresh = async () => {
    try {
      const data = await apiFetch("/api/auth/refresh", { method: "POST", body: "{}" });
      setAccessToken(data.access);
      await loadMe(data.access);
      return true;
    } catch {
      setAccessToken("");
      setUser(null);
      return false;
    }
  };

  useEffect(() => {
    refresh().finally(() => setLoading(false));
  }, []);

  const login = async (email, password) => {
    const data = await apiFetch("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password })
    });
    setAccessToken(data.access);
    setUser(data.user);
    return data.user;
  };

  const register = async (email, password, favorite_club) => {
    const data = await apiFetch("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, favorite_club })
    });
    return data.user;
  };

  const logout = () => {
    setAccessToken("");
    setUser(null);
  };

  const updateFavoriteClub = async (favorite_club) => {
    const data = await apiFetch(
      "/api/me",
      { method: "PATCH", body: JSON.stringify({ favorite_club }) },
      accessToken
    );
    setUser(data);
    return data;
  };

  const value = useMemo(
    () => ({
      accessToken,
      user,
      loading,
      login,
      register,
      logout,
      refresh,
      updateFavoriteClub
    }),
    [accessToken, user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
