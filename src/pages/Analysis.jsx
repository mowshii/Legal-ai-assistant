/**
 * pages/Analysis.jsx
 * ------------------------
 * Module 21 — Main Analysis Dashboard.
 * Sections: Document Overview, Extracted Information, Verification,
 * Risk Analysis, Evidence, language switch, download report.
 *
 * Dependencies: services/documents, react-router-dom
 */
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Download, Eye } from "lucide-react";
import {
  getDocument, getAnalysis, getRisks, getEvidence, getReport,
} from "../services/documents";
import RiskBadge from "../components/RiskBadge";
import EvidenceModal from "../components/EvidenceModal";
import { useLanguage } from "../context/LanguageContext";

const SECTION_LABELS = {
  document_information: "Document Information",
  seller: "Seller",
  buyer: "Buyer",
  property: "Property",
  financial_information: "Financial Information",
};

export default function Analysis() {
  const { id } = useParams();
  const { t } = useLanguage();

  const [document, setDocument] = useState(null);
  const [extracted, setExtracted] = useState(null);
  const [risks, setRisks] = useState([]);
  const [evidence, setEvidence] = useState([]);
  const [evidenceItem, setEvidenceItem] = useState(null);
  const [notReady, setNotReady] = useState(false);

  useEffect(() => {
    getDocument(id).then((res) => setDocument(res.data)).catch(() => {});
    getAnalysis(id).then((res) => setExtracted(res.data)).catch(() => setNotReady(true));
    getRisks(id).then((res) => setRisks(res.data)).catch(() => {});
    getEvidence(id).then((res) => setEvidence(res.data)).catch(() => {});
  }, [id]);

  const findEvidence = (fieldPath) => evidence.find((e) => e.field === fieldPath);

  const handleDownload = async () => {
    const { data } = await getReport(id);
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = window.document.createElement("a");
    a.href = url;
    a.download = `sales-deed-report-${id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (notReady) {
    return (
      <div className="max-w-3xl">
        <p className="text-ink/60">
          This document hasn't been analyzed yet, or the backend/Ollama pipeline isn't
          running. Trigger analysis from the Upload page, or check that the Flask API
          and Ollama are running.
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl">
      <EvidenceModal item={evidenceItem} onClose={() => setEvidenceItem(null)} />

      {/* --- Document Overview --- */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <h1 className="font-display text-3xl text-ink mb-1">{t("documentOverview")}</h1>
          <p className="text-ink/60 text-sm">
            {document?.original_filename} · {document?.page_count ?? "—"} pages
            {document?.ocr_used ? " · OCR used" : ""}
          </p>
        </div>
        <button
          onClick={handleDownload}
          className="flex items-center gap-2 px-5 py-2.5 bg-manuscript text-paper rounded-full font-semibold hover:bg-manuscript-dark transition-colors"
        >
          <Download size={16} /> {t("downloadReport")}
        </button>
      </div>

      {/* --- Extracted Information --- */}
      <Section title={t("extractedInformation")}>
        {extracted && Object.entries(SECTION_LABELS).map(([key, label]) => (
          <div key={key} className="mb-6 last:mb-0">
            <h3 className="text-sm font-semibold text-manuscript uppercase tracking-wide mb-2">{label}</h3>
            <table className="w-full text-sm">
              <tbody>
                {Object.entries(extracted[key] || {}).map(([field, value]) => {
                  const fieldPath = `${key}.${field}`;
                  const ev = findEvidence(fieldPath);
                  return (
                    <tr key={field} className="border-b border-manuscript/8 last:border-0">
                      <td className="py-2 pr-4 text-ink/60 w-1/3 capitalize">{field.replaceAll("_", " ")}</td>
                      <td className="py-2 pr-4 text-ink font-medium">{value || t("notFound")}</td>
                      <td className="py-2 text-right">
                        {ev && (
                          <button
                            onClick={() => setEvidenceItem(ev)}
                            className="inline-flex items-center gap-1 text-xs text-manuscript hover:underline"
                          >
                            <Eye size={12} /> {t("viewEvidence")}
                          </button>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ))}
      </Section>

      {/* --- Verification --- */}
      <Section title={t("verification")}>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-ink/50 border-b border-manuscript/15">
              <th className="py-2 font-medium">{t("field")}</th>
              <th className="py-2 font-medium">{t("value")}</th>
              <th className="py-2 font-medium">{t("confidence")}</th>
              <th className="py-2 font-medium">{t("source")}</th>
            </tr>
          </thead>
          <tbody>
            {evidence.map((e) => (
              <tr key={e.field} className="border-b border-manuscript/8 last:border-0">
                <td className="py-2 pr-4 capitalize">{e.field.replace(".", " · ").replaceAll("_", " ")}</td>
                <td className="py-2 pr-4 font-medium">{e.extracted_value || t("notFound")}</td>
                <td className="py-2 pr-4">{e.confidence}</td>
                <td className="py-2">{e.evidence_page ? `Page ${e.evidence_page}` : "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>

      {/* --- Risk Analysis --- */}
      <Section title={t("riskAnalysis")}>
        {risks.length === 0 && <p className="text-ink/50 text-sm">No risks flagged for this document.</p>}
        <div className="space-y-4">
          {risks.map((r, i) => (
            <div key={i} className="border border-manuscript/12 rounded-xl p-4">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold text-ink">{r.risk}</h4>
                <RiskBadge level={r.risk_level} />
              </div>
              <p className="text-sm text-ink/70 mb-2">{r.explanation}</p>
              <p className="text-xs text-ink/50 mb-2">{t("evidence")}: {r.evidence || "Insufficient Evidence"}</p>
              <div className="grid sm:grid-cols-2 gap-3 mt-3">
                <div className="bg-parchment/60 rounded-lg p-3">
                  <p className="text-xs font-semibold text-manuscript mb-1">{t("recommendedAction")}</p>
                  <p className="text-sm text-ink/80">{r.recommended_action}</p>
                </div>
                <div className="bg-parchment/60 rounded-lg p-3">
                  <p className="text-xs font-semibold text-manuscript mb-1">{t("possibleResolution")}</p>
                  <p className="text-sm text-ink/80">{r.possible_resolution}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Section>

      <p className="text-xs text-ink/40 mt-2 mb-10">{t("disclaimer")}</p>
    </div>
  );
}

function Section({ title, children }) {
  return (
    <div className="bg-paper rounded-2xl shadow-paper p-6 mb-6">
      <h2 className="font-display text-xl text-ink mb-4">{title}</h2>
      {children}
    </div>
  );
}
