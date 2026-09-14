/**
 * pages/Login.jsx
 * --------------------
 */
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { FileCheck2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.error || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-parchment flex items-center justify-center px-4">
      <div className="bg-paper rounded-2xl shadow-paper p-8 w-full max-w-sm">
        <div className="flex items-center gap-2 justify-center mb-6">
          <FileCheck2 className="text-seal" size={22} />
          <span className="font-display text-lg text-ink">Aavanam AI</span>
        </div>

        <h1 className="font-display text-2xl text-center mb-6">Log in</h1>

        {error && <p className="text-seal text-sm mb-4 text-center">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="email" required placeholder="Email" value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-2.5 rounded-xl border border-manuscript/20 bg-parchment/40 focus:outline-none focus:ring-2 focus:ring-manuscript/40"
          />
          <input
            type="password" required placeholder="Password" value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2.5 rounded-xl border border-manuscript/20 bg-parchment/40 focus:outline-none focus:ring-2 focus:ring-manuscript/40"
          />
          <button
            type="submit" disabled={loading}
            className="w-full py-2.5 bg-manuscript text-paper rounded-xl font-semibold hover:bg-manuscript-dark transition-colors disabled:opacity-60"
          >
            {loading ? "Logging in…" : "Log in"}
          </button>
        </form>

        <p className="text-sm text-ink/60 text-center mt-6">
          No account yet?{" "}
          <Link to="/register" className="text-manuscript font-semibold">Create one</Link>
        </p>
      </div>
    </div>
  );
}
