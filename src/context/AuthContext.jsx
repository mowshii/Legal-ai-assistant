/**
 * context/AuthContext.jsx
 * --------------------------
 * Holds the logged-in user + token, exposes login/register/logout.
 * Token persists in localStorage so a page refresh doesn't log you out.
 *
 * Dependencies: react, services/api
 */
import { createContext, useContext, useState, useCallback } from "react";
import api from "../services/api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem("aavanam_user");
    return raw ? JSON.parse(raw) : null;
  });

  const persist = (token, user) => {
    localStorage.setItem("aavanam_token", token);
    localStorage.setItem("aavanam_user", JSON.stringify(user));
    setUser(user);
  };

  const login = useCallback(async (email, password) => {
    const { data } = await api.post("/auth/login", { email, password });
    persist(data.token, data.user);
    return data.user;
  }, []);

  const register = useCallback(async (name, email, password) => {
    const { data } = await api.post("/auth/register", { name, email, password });
    persist(data.token, data.user);
    return data.user;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("aavanam_token");
    localStorage.removeItem("aavanam_user");
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
