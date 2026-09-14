/**
 * components/LanguageSwitcher.jsx
 * -----------------------------------
 * Module 23 — EN | தமிழ் switcher. Switching does not re-upload or
 * re-analyze the document; it just changes displayed language.
 */
import { useLanguage } from "../context/LanguageContext";

export default function LanguageSwitcher() {
  const { language, setLanguage } = useLanguage();
  return (
    <div className="inline-flex rounded-full border border-manuscript/30 bg-paper overflow-hidden text-sm font-semibold">
      <button
        onClick={() => setLanguage("en")}
        className={`px-4 py-1.5 transition-colors ${
          language === "en" ? "bg-manuscript text-paper" : "text-manuscript hover:bg-manuscript/10"
        }`}
      >
        EN
      </button>
      <button
        onClick={() => setLanguage("ta")}
        className={`px-4 py-1.5 transition-colors ${
          language === "ta" ? "bg-manuscript text-paper" : "text-manuscript hover:bg-manuscript/10"
        }`}
      >
        தமிழ்
      </button>
    </div>
  );
}
