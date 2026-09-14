/**
 * pages/Documents.jsx
 * ------------------------
 */
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { FileText, Trash2 } from "lucide-react";
import { listDocuments, deleteDocument } from "../services/documents";
import { useLanguage } from "../context/LanguageContext";

export default function Documents() {
  const { t } = useLanguage();
  const [documents, setDocuments] = useState([]);

  const load = () => listDocuments().then((res) => setDocuments(res.data)).catch(() => {});
  useEffect(() => { load(); }, []);

  const handleDelete = async (id) => {
    await deleteDocument(id);
    load();
  };

  return (
    <div className="max-w-5xl">
      <h1 className="font-display text-3xl text-ink mb-8">{t("documents")}</h1>

      <div className="bg-paper rounded-2xl shadow-paper divide-y divide-manuscript/10">
        {documents.length === 0 && (
          <p className="p-6 text-ink/50 text-sm">No documents uploaded yet.</p>
        )}
        {documents.map((doc) => (
          <div key={doc.document_id} className="flex items-center justify-between px-6 py-4">
            <Link to={`/analysis/${doc.document_id}`} className="flex items-center gap-3 flex-1 hover:opacity-80">
              <FileText className="text-manuscript" size={18} />
              <div>
                <p className="font-medium text-ink text-sm">{doc.original_filename}</p>
                <p className="text-xs text-ink/50">
                  {doc.page_count ?? "—"} pages · {(doc.file_size_bytes / 1024 / 1024).toFixed(2)} MB · {doc.status}
                </p>
              </div>
            </Link>
            <button onClick={() => handleDelete(doc.document_id)} className="text-ink/30 hover:text-seal transition-colors">
              <Trash2 size={18} />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
