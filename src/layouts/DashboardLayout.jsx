/**
 * layouts/DashboardLayout.jsx
 * -------------------------------
 * Sidebar + topbar shell for every authenticated page (Module 19 pages).
 * Deliberately minimal — no crowded card grid, per the "clean, minimalist"
 * requirement.
 */
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { LayoutDashboard, Upload, Files, History, User, Shield, LogOut, FileCheck2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";
import { useLanguage } from "../context/LanguageContext";
import LanguageSwitcher from "../components/LanguageSwitcher";

export default function DashboardLayout() {
  const { user, logout } = useAuth();
  const { t } = useLanguage();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const navItem = (to, icon, label) => (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-colors ${
          isActive ? "bg-manuscript text-paper" : "text-ink/70 hover:bg-manuscript/10"
        }`
      }
    >
      {icon}
      {label}
    </NavLink>
  );

  return (
    <div className="min-h-screen flex bg-parchment">
      <aside className="w-64 bg-paper border-r border-manuscript/15 flex flex-col p-5 shrink-0">
        <div className="flex items-center gap-2 mb-8 px-1">
          <FileCheck2 className="text-seal" size={24} />
          <span className="font-display text-lg text-ink">{t("appName")}</span>
        </div>

        <nav className="flex flex-col gap-1 flex-1">
          {navItem("/dashboard", <LayoutDashboard size={18} />, t("dashboard"))}
          {navItem("/upload", <Upload size={18} />, t("upload"))}
          {navItem("/documents", <Files size={18} />, t("documents"))}
          {navItem("/history", <History size={18} />, t("history"))}
          {navItem("/profile", <User size={18} />, t("profile"))}
          {user?.role === "admin" && navItem("/admin", <Shield size={18} />, t("admin"))}
        </nav>

        <button
          onClick={handleLogout}
          className="flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium text-ink/60 hover:bg-seal/10 hover:text-seal transition-colors"
        >
          <LogOut size={18} />
          {t("logout")}
        </button>
      </aside>

      <div className="flex-1 flex flex-col">
        <header className="h-16 flex items-center justify-end gap-4 px-8 border-b border-manuscript/15 bg-paper/60">
          <LanguageSwitcher />
          <div className="w-9 h-9 rounded-full bg-manuscript text-paper flex items-center justify-center font-semibold text-sm">
            {(user?.name || "U").charAt(0).toUpperCase()}
          </div>
        </header>
        <main className="flex-1 p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
