/**
 * pages/Dashboard.jsx
 * ------------------------
 * Module 19 — main dashboard: upload CTA, recent documents, analysis
 * statistics, recent risk results. Kept intentionally uncluttered.
 *
 * Dependencies: services/documents
 */
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Upload, FileText, AlertTriangle } from "lucide-react";
import { listDocuments } from "../services/documents";
import RiskBadge from "../components/RiskBadge";
import { useLanguage } from "../context/LanguageContext";

export default function Dashboard() {
  const { t } = useLanguage();
  const [documents, setDocuments] = useState([]);
  const [loadError, setLoadError] = useState("");

  useEffect(() => {
    listDocuments()
      .then((res) => setDocuments(res.data))
      .catch(() => setLoadError("Could not reach the backend yet — start the Flask API to see live data."));
  }, []);

  const completed = documents.filter((d) => d.status === "completed").length;

  return (
    <div className="max-w-5xl">
      <div className="flex items-center justify-between mb-8">
        <h1 className="font-display text-3xl text-ink">{t("dashboard")}</h1>
        <Link
          to="/upload"
          className="flex items-center gap-2 px-5 py-2.5 bg-seal text-paper rounded-full font-semibold hover:bg-seal-light transition-colors"
        >
          <Upload size={18} /> {t("upload")}
        </Link>
      </div>

      {loadError && (
        <div className="bg-ochre/10 border border-ochre/30 text-ochre rounded-xl p-4 mb-6 text-sm">
          {loadError}
        </div>
      )}

      <div className="grid md:grid-cols-3 gap-5 mb-10">
        <StatCard label="Documents uploaded" value={documents.length} />
        <StatCard label="Analyses completed" value={completed} />
        <StatCard label="Awaiting analysis" value={documents.length - completed} />
      </div>

      <h2 className="font-display text-xl mb-4">{t("recentDocuments")}</h2>
      <div className="bg-paper rounded-2xl shadow-paper divide-y divide-manuscript/10">
        {documents.length === 0 && (
          <p className="p-6 text-ink/50 text-sm">
            No documents yet. Upload a Sales Deed PDF to get started.
          </p>
        )}
        {documents.slice(0, 6).map((doc) => (
          <Link
            key={doc.document_id}
            to={`/analysis/${doc.document_id}`}
            className="flex items-center justify-between px-6 py-4 hover:bg-manuscript/5 transition-colors"
          >
            <div className="flex items-center gap-3">
              <FileText className="text-manuscript" size={18} />
              <div>
                <p className="font-medium text-ink text-sm">{doc.original_filename}</p>
                <p className="text-xs text-ink/50">{doc.page_count ?? "—"} pages · {doc.status}</p>
              </div>
            </div>
            {doc.status === "failed" && (
              <span className="flex items-center gap-1 text-seal text-xs font-semibold">
                <AlertTriangle size={14} /> Failed
              </span>
            )}
          </Link>
        ))}
      </div>
    </div>
  );
}

function StatCard({ label, value }) {
  return (
    <div className="bg-paper rounded-2xl shadow-paper p-5">
      <p className="text-sm text-ink/50 mb-1">{label}</p>
      <p className="font-display text-3xl text-ink">{value}</p>
    </div>
  );
}
