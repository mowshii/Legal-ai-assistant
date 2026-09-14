/**
 * pages/Register.jsx
 * -----------------------
 */
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { FileCheck2 } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const update = (key) => (e) => setForm({ ...form, [key]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await register(form.name, form.email, form.password);
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

        <h1 className="font-display text-2xl text-center mb-6">Create your account</h1>

        {error && <p className="text-seal text-sm mb-4 text-center">{error}</p>}

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            required placeholder="Full name" value={form.name} onChange={update("name")}
            className="w-full px-4 py-2.5 rounded-xl border border-manuscript/20 bg-parchment/40 focus:outline-none focus:ring-2 focus:ring-manuscript/40"
          />
          <input
            type="email" required placeholder="Email" value={form.email} onChange={update("email")}
            className="w-full px-4 py-2.5 rounded-xl border border-manuscript/20 bg-parchment/40 focus:outline-none focus:ring-2 focus:ring-manuscript/40"
          />
          <input
            type="password" required placeholder="Password" value={form.password} onChange={update("password")}
            className="w-full px-4 py-2.5 rounded-xl border border-manuscript/20 bg-parchment/40 focus:outline-none focus:ring-2 focus:ring-manuscript/40"
          />
          <button
            type="submit" disabled={loading}
            className="w-full py-2.5 bg-manuscript text-paper rounded-xl font-semibold hover:bg-manuscript-dark transition-colors disabled:opacity-60"
          >
            {loading ? "Creating account…" : "Create account"}
          </button>
        </form>

        <p className="text-sm text-ink/60 text-center mt-6">
          Already have an account?{" "}
          <Link to="/login" className="text-manuscript font-semibold">Log in</Link>
        </p>
      </div>
    </div>
  );
}
