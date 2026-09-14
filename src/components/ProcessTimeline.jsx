/**
 * components/ProcessTimeline.jsx
 * ----------------------------------
 * Module 20 — AI processing timeline shown after upload.
 * Numbering IS justified here — these steps are a genuine fixed sequence,
 * not decorative markers.
 */
const STEPS = [
  "Uploading",
  "Reading PDF",
  "Extracting information",
  "Retrieving evidence",
  "Verifying data",
  "Analyzing risks",
  "Generating report",
];

export default function ProcessTimeline({ currentStep = 0 }) {
  return (
    <ol className="space-y-3">
      {STEPS.map((step, i) => {
        const done = i < currentStep;
        const active = i === currentStep;
        return (
          <li key={step} className="flex items-center gap-3">
            <span
              className={`flex items-center justify-center w-7 h-7 rounded-full text-xs font-semibold shrink-0 ${
                done
                  ? "bg-moss text-paper"
                  : active
                  ? "bg-seal text-paper animate-pulse"
                  : "bg-parchment border border-manuscript/30 text-manuscript/50"
              }`}
            >
              {i + 1}
            </span>
            <span className={done || active ? "text-ink font-medium" : "text-ink/40"}>{step}</span>
          </li>
        );
      })}
    </ol>
  );
}
