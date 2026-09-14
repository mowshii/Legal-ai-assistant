/**
 * pages/Upload.jsx
 * ---------------------
 * Modules 2 & 20 — upload interface + AI processing timeline.
 * Validates client-side first (extension/size) for instant feedback, then
 * lets the backend do the authoritative validation (MIME sniff + PDF open).
 *
 * Dependencies: services/documents
 */
import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { UploadCloud, FileText } from "lucide-react";
import { uploadDocument, analyzeDocument } from "../services/documents";
import ProcessTimeline from "../components/ProcessTimeline";
import { useLanguage } from "../context/LanguageContext";

const MAX_SIZE = 10 * 1024 * 1024;

export default function Upload() {
  const { t, language } = useLanguage();
  const navigate = useNavigate();
  const inputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [step, setStep] = useState(-1); // -1 = not started
  const [dragOver, setDragOver] = useState(false);

  const validateAndSet = (candidate) => {
    setError("");
    if (!candidate) return;
    if (candidate.type !== "application/pdf" && !candidate.name.toLowerCase().endsWith(".pdf")) {
      setError("Only PDF files are supported.");
      return;
    }
    if (candidate.size === 0) {
      setError("The uploaded file is empty.");
      return;
    }
    if (candidate.size > MAX_SIZE) {
      setError("Maximum file size is 10 MB.");
      return;
    }
    setFile(candidate);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    validateAndSet(e.dataTransfer.files?.[0]);
  };

  const handleUploadAndAnalyze = async () => {
    if (!file) return;
    setError("");
    setStep(0);
    try {
      const { data: doc } = await uploadDocument(file);
      setStep(1);
      // The real pipeline runs server-side inside the LangGraph workflow;
      // this client-side timeline is a UI approximation of that same sequence
      // (Module 20) so the user isn't staring at a blank screen while it runs.
      const tick = (n) => new Promise((res) => setTimeout(() => { setStep(n); res(); }, 900));
      await tick(2); await tick(3); await tick(4); await tick(5);
      await analyzeDocument(doc.document_id, language);
      setStep(6);
      setTimeout(() => navigate(`/analysis/${doc.document_id}`), 600);
    } catch (err) {
      setError(err.response?.data?.error || "The uploaded PDF could not be processed.");
      setStep(-1);
    }
  };

  return (
    <div className="max-w-2xl">
      <h1 className="font-display text-3xl text-ink mb-2">{t("uploadCta")}</h1>
      <p className="text-ink/60 mb-8">{t("maxSize")} · {t("allowedFormat")}</p>

      {step === -1 && (
        <>
          <div
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
            className={`bg-paper rounded-2xl border-2 border-dashed p-12 text-center cursor-pointer transition-colors ${
              dragOver ? "border-seal bg-seal/5" : "border-manuscript/25"
            }`}
          >
            <input
              ref={inputRef} type="file" accept="application/pdf" className="hidden"
              onChange={(e) => validateAndSet(e.target.files?.[0])}
            />
            {file ? (
              <div className="flex flex-col items-center gap-2">
                <FileText className="text-manuscript" size={36} />
                <p className="font-medium text-ink">{file.name}</p>
                <p className="text-sm text-ink/50">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            ) : (
              <div className="flex flex-col items-center gap-2 text-ink/50">
                <UploadCloud size={36} />
                <p>Drag and drop your Sales Deed PDF here, or click to browse</p>
              </div>
            )}
          </div>

          {error && <p className="text-seal text-sm mt-4">{error}</p>}

          <button
            disabled={!file}
            onClick={handleUploadAndAnalyze}
            className="mt-6 px-6 py-3 bg-manuscript text-paper rounded-full font-semibold hover:bg-manuscript-dark transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            Upload and analyze
          </button>
        </>
      )}

      {step >= 0 && (
        <div className="bg-paper rounded-2xl shadow-paper p-8">
          <ProcessTimeline currentStep={step} />
          {error && <p className="text-seal text-sm mt-4">{error}</p>}
        </div>
      )}
    </div>
  );
}
