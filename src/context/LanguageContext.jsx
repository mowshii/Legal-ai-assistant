/**
 * context/LanguageContext.jsx
 * -------------------------------
 * Module 23 — Tamil + English UI.
 * Holds the current UI language and a small static dictionary for chrome
 * (nav, buttons, table headers, risk labels) — this is instant and free.
 * Actual DOCUMENT analysis text is translated by the backend Translation
 * Agent (Module 12) via services/documents.getTranslation, since that
 * content doesn't exist until a document has been analyzed.
 *
 * Dependencies: react
 */
import { createContext, useContext, useState } from "react";

const STRINGS = {
  en: {
    appName: "Aavanam AI",
    tagline: "AI-assisted Sales Deed analysis",
    dashboard: "Dashboard",
    upload: "Upload Sales Deed",
    documents: "Documents",
    history: "History",
    profile: "Profile",
    admin: "Admin",
    logout: "Log out",
    login: "Log in",
    register: "Create account",
    uploadCta: "Upload Sales Deed PDF",
    maxSize: "Maximum size: 10 MB",
    allowedFormat: "Allowed format: PDF",
    recentDocuments: "Recent documents",
    analysisStats: "Analysis statistics",
    recentRisks: "Recent risk results",
    documentOverview: "Document overview",
    extractedInformation: "Extracted information",
    verification: "Verification",
    riskAnalysis: "Risk analysis",
    evidence: "Evidence",
    downloadReport: "Download report",
    viewEvidence: "View evidence",
    source: "Source",
    confidence: "Confidence",
    field: "Field",
    value: "Value",
    riskLevel: "Risk level",
    explanation: "Explanation",
    recommendedAction: "Recommended verification",
    possibleResolution: "Possible resolution",
    disclaimer:
      "AI-assisted findings only. Not legal advice — verify with a qualified legal professional.",
    low: "LOW", medium: "MEDIUM", high: "HIGH",
    notFound: "Not Found",
  },
  ta: {
    appName: "ஆவணம் AI",
    tagline: "AI உதவியுடன் கிரய பத்திர பகுப்பாய்வு",
    dashboard: "டாஷ்போர்டு",
    upload: "கிரய பத்திரத்தை பதிவேற்றவும்",
    documents: "ஆவணங்கள்",
    history: "வரலாறு",
    profile: "சுயவிவரம்",
    admin: "நிர்வாகி",
    logout: "வெளியேறு",
    login: "உள்நுழையவும்",
    register: "கணக்கை உருவாக்கவும்",
    uploadCta: "கிரய பத்திர PDF ஐ பதிவேற்றவும்",
    maxSize: "அதிகபட்ச அளவு: 10 MB",
    allowedFormat: "அனுமதிக்கப்பட்ட வடிவம்: PDF",
    recentDocuments: "சமீபத்திய ஆவணங்கள்",
    analysisStats: "பகுப்பாய்வு புள்ளிவிவரங்கள்",
    recentRisks: "சமீபத்திய இடர் முடிவுகள்",
    documentOverview: "ஆவண மேலோட்டம்",
    extractedInformation: "பிரித்தெடுக்கப்பட்ட தகவல்",
    verification: "சரிபார்ப்பு",
    riskAnalysis: "இடர் பகுப்பாய்வு",
    evidence: "ஆதாரம்",
    downloadReport: "அறிக்கையைப் பதிவிறக்கவும்",
    viewEvidence: "ஆதாரத்தைப் பார்க்கவும்",
    source: "மூலம்",
    confidence: "நம்பகத்தன்மை",
    field: "புலம்",
    value: "மதிப்பு",
    riskLevel: "இடர் நிலை",
    explanation: "விளக்கம்",
    recommendedAction: "பரிந்துரைக்கப்பட்ட சரிபார்ப்பு",
    possibleResolution: "சாத்தியமான தீர்வு",
    disclaimer:
      "இவை AI உதவியுடன் கண்டறியப்பட்டவை மட்டுமே. இது சட்ட ஆலோசனை அல்ல — தகுதியான சட்ட நிபுணரிடம் சரிபார்க்கவும்.",
    low: "குறைவு", medium: "நடுத்தரம்", high: "அதிகம்",
    notFound: "கிடைக்கவில்லை",
  },
};

const LanguageContext = createContext(null);

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState("en");
  const t = (key) => STRINGS[language][key] ?? key;
  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export const useLanguage = () => useContext(LanguageContext);
