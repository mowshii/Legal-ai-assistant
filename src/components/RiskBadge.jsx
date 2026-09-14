/**
 * components/RiskBadge.jsx
 * ---------------------------
 * Consistent LOW/MEDIUM/HIGH pill used in risk cards, reports, and the
 * dashboard summary. Color is the only semantic carrier of severity here,
 * so the label text itself is always shown too (never color-only).
 */
import { useLanguage } from "../context/LanguageContext";

const STYLES = {
  LOW: "bg-moss/15 text-moss border border-moss/40",
  MEDIUM: "bg-ochre/15 text-ochre border border-ochre/40",
  HIGH: "bg-seal/15 text-seal border border-seal/40",
};

export default function RiskBadge({ level }) {
  const { t } = useLanguage();
  const label = { LOW: t("low"), MEDIUM: t("medium"), HIGH: t("high") }[level] || level;
  return (
    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold ${STYLES[level] || STYLES.MEDIUM}`}>
      {label}
    </span>
  );
}
