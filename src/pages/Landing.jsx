/**
 * pages/Landing.jsx
 * ---------------------
 * Public marketing page. Opens with the most characteristic thing in this
 * product's world: a document being examined and stamped — realized as
 * the rotating 3D wax seal, not a generic gradient hero.
 */
import { Link } from "react-router-dom";
import { ScanSearch, ShieldAlert, Languages, Database } from "lucide-react";
import HeroSeal from "../components/HeroSeal";

const PIPELINE = [
  "Upload the Sales Deed PDF",
  "Extract and clean the document text",
  "Retrieve relevant evidence with RAG",
  "Extract and verify structured fields",
  "Flag and classify potential risks",
  "Read the bilingual report",
];

export default function Landing() {
  return (
    <div className="min-h-screen bg-parchment text-ink">
      <header className="flex items-center justify-between px-8 py-6 max-w-6xl mx-auto">
        <span className="font-display text-xl">Aavanam AI</span>
        <div className="flex gap-3">
          <Link to="/login" className="px-5 py-2 text-sm font-medium text-ink/70 hover:text-ink">
            Log in
          </Link>
          <Link to="/register" className="px-5 py-2 text-sm font-semibold bg-seal text-paper rounded-full hover:bg-seal-light">
            Create account
          </Link>
        </div>
      </header>

      <section className="max-w-6xl mx-auto px-8 pt-10 pb-20 grid md:grid-cols-2 gap-12 items-center">
        <div>
          <h1 className="font-display text-5xl leading-[1.1] mb-6">
            Read every Sales Deed like a careful second pair of eyes.
          </h1>
          <p className="text-lg text-ink/70 mb-8 max-w-md">
            Upload a property Sales Deed and get the parties, property details, and
            consideration pulled into a table — with every field traced back to the
            page it came from, and any inconsistencies flagged for a professional to review.
          </p>
          <Link
            to="/register"
            className="inline-block px-7 py-3 bg-manuscript text-paper rounded-full font-semibold hover:bg-manuscript-dark transition-colors"
          >
            Analyze your first deed
          </Link>
          <p className="text-sm text-ink/50 mt-4 max-w-md">
            AI-assisted findings only — not legal advice. Results require verification
            by a qualified legal professional.
          </p>
        </div>
        <HeroSeal />
      </section>

      <section className="max-w-6xl mx-auto px-8 pb-20">
        <h2 className="font-display text-2xl mb-8">What happens to your document</h2>
        <ol className="grid md:grid-cols-3 gap-5">
          {PIPELINE.map((step, i) => (
            <li key={step} className="bg-paper rounded-2xl p-5 shadow-paper">
              <span className="text-seal font-display text-2xl">{i + 1}</span>
              <p className="mt-2 text-ink/80">{step}</p>
            </li>
          ))}
        </ol>
      </section>

      <section className="max-w-6xl mx-auto px-8 pb-24 grid md:grid-cols-4 gap-6">
        <Feature icon={<ScanSearch size={22} />} title="Evidence-based" text="Every field links back to the page it was found on." />
        <Feature icon={<ShieldAlert size={22} />} title="Risk flagged, not judged" text="Findings are marked LOW, MEDIUM, or HIGH for review — never a legal verdict." />
        <Feature icon={<Languages size={22} />} title="English & Tamil" text="Switch languages without re-uploading the document." />
        <Feature icon={<Database size={22} />} title="Runs on your own data" text="Local LLM via Ollama — your deed never leaves your infrastructure." />
      </section>
    </div>
  );
}

function Feature({ icon, title, text }) {
  return (
    <div>
      <div className="text-manuscript mb-3">{icon}</div>
      <h3 className="font-semibold mb-1">{title}</h3>
      <p className="text-sm text-ink/60">{text}</p>
    </div>
  );
}
