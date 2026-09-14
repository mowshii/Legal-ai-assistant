/**
 * components/EvidenceModal.jsx
 * --------------------------------
 * Module 22 — Evidence-Based UI. Clicking "View Evidence" on a field
 * opens this modal showing the page number and (if available) the
 * retrieved excerpt that supports the extracted value.
 */
import { X } from "lucide-react";
import { useLanguage } from "../context/LanguageContext";

export default function EvidenceModal({ item, onClose }) {
  const { t } = useLanguage();
  if (!item) return null;

  return (
    <div className="fixed inset-0 bg-ink/40 flex items-center justify-center p-4 z-50" onClick={onClose}>
      <div
        className="bg-paper rounded-2xl shadow-paper max-w-md w-full p-6"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between mb-4">
          <h3 className="font-display text-xl text-ink">{item.field}</h3>
          <button onClick={onClose} className="text-ink/50 hover:text-ink">
            <X size={20} />
          </button>
        </div>
        <p className="text-ink/70 text-sm mb-1">{t("value")}</p>
        <p className="font-medium text-ink mb-4">{item.extracted_value || t("notFound")}</p>

        <p className="text-ink/70 text-sm mb-1">{t("source")}</p>
        <p className="font-medium text-ink mb-4">
          {item.evidence_page ? `Page ${item.evidence_page}` : "—"}
        </p>

        <p className="text-ink/70 text-sm mb-1">{t("confidence")}</p>
        <p className="font-medium text-ink">{item.confidence || "—"}</p>
      </div>
    </div>
  );
}
