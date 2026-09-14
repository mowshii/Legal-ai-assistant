/**
 * pages/History.jsx
 * -----------------------
 * Module 19 /history — a user's own past analyses, most recent first.
 * Reuses the same document list endpoint as Documents.jsx but framed
 * around "past analysis runs" rather than file management.
 */
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { listDocuments } from "../services/documents";
import RiskBadge from "../components/RiskBadge";

export default function History() {
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    listDocuments().then((res) => setDocuments(res.data)).catch(() => {});
  }, []);

  const analyzed = documents.filter((d) => d.status === "completed" || d.status === "failed");

  return (
    <div className="max-w-4xl">
      <h1 className="font-display text-3xl text-ink mb-8">History</h1>
      <div className="bg-paper rounded-2xl shadow-paper divide-y divide-manuscript/10">
        {analyzed.length === 0 && (
          <p className="p-6 text-ink/50 text-sm">No completed analyses yet.</p>
        )}
        {analyzed.map((doc) => (
          <Link
            key={doc.document_id}
            to={`/analysis/${doc.document_id}`}
            className="flex items-center justify-between px-6 py-4 hover:bg-manuscript/5 transition-colors"
          >
            <div>
              <p className="font-medium text-ink text-sm">{doc.original_filename}</p>
              <p className="text-xs text-ink/50">{new Date(doc.created_at).toLocaleString()}</p>
            </div>
            {doc.status === "failed" ? (
              <span className="text-seal text-xs font-semibold">Failed</span>
            ) : (
              <RiskBadge level="LOW" />
            )}
          </Link>
        ))}
      </div>
    </div>
  );
}
