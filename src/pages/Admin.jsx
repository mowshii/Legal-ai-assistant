/**
 * pages/Admin.jsx
 * ---------------------
 * Module 1 — Admin view: all users' uploaded documents and analysis
 * history. GET /api/documents already returns every document when the
 * caller's role is 'admin' (see routes/document_routes.py), so this page
 * simply reuses that endpoint.
 */
import { useEffect, useState } from "react";
import { listDocuments } from "../services/documents";

export default function Admin() {
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    listDocuments().then((res) => setDocuments(res.data)).catch(() => {});
  }, []);

  return (
    <div className="max-w-5xl">
      <h1 className="font-display text-3xl text-ink mb-2">Admin</h1>
      <p className="text-ink/60 mb-8">All documents uploaded across every user account.</p>

      <div className="bg-paper rounded-2xl shadow-paper overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-ink/50 bg-parchment/50">
              <th className="py-3 px-6 font-medium">File</th>
              <th className="py-3 px-6 font-medium">Pages</th>
              <th className="py-3 px-6 font-medium">Status</th>
              <th className="py-3 px-6 font-medium">Uploaded</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc) => (
              <tr key={doc.document_id} className="border-t border-manuscript/8">
                <td className="py-3 px-6">{doc.original_filename}</td>
                <td className="py-3 px-6">{doc.page_count ?? "—"}</td>
                <td className="py-3 px-6 capitalize">{doc.status}</td>
                <td className="py-3 px-6">{new Date(doc.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
