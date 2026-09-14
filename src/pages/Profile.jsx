/**
 * pages/Profile.jsx
 * -----------------------
 * Module 19 /profile — basic account info, read-only for now.
 */
import { useAuth } from "../context/AuthContext";

export default function Profile() {
  const { user } = useAuth();

  return (
    <div className="max-w-md">
      <h1 className="font-display text-3xl text-ink mb-8">Profile</h1>
      <div className="bg-paper rounded-2xl shadow-paper p-6 space-y-4">
        <Field label="Name" value={user?.name} />
        <Field label="Email" value={user?.email} />
        <Field label="Role" value={user?.role} />
      </div>
    </div>
  );
}

function Field({ label, value }) {
  return (
    <div>
      <p className="text-xs text-ink/50 uppercase tracking-wide mb-1">{label}</p>
      <p className="text-ink font-medium">{value || "—"}</p>
    </div>
  );
}
