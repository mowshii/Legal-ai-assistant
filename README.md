# Aavanam AI — Intelligent Bilingual Sales Deed Analysis System

An AI-assisted document intelligence platform for Indian real-estate Sales Deeds.
It extracts structured information, verifies it against the source PDF, flags
potential risks (LOW / MEDIUM / HIGH), and presents everything bilingually
(English / Tamil).

> **This system does not provide legal advice.** Every finding is an AI-assisted
> observation that requires verification by a qualified legal professional.

---

## 1. What's included vs. what you need to install

This repo contains **all the application code** — frontend, backend, database
models, LangGraph agents, and prompts. Three pieces of infrastructure run
*outside* this repo, on your own machine, because they need real compute
(a GPU/CPU for the LLM, a running database server):

| Piece | What it's for | You install it |
|---|---|---|
| **PostgreSQL + pgvector** | stores users, documents, chunks, embeddings, results | locally or via Docker |
| **Ollama + Qwen3 8B** | the local LLM every agent calls | locally |
| **Tesseract OCR** | reads scanned/image-only PDF pages | locally |

Everything else (Flask API, React frontend, LangGraph graph, all 7 agents) is
written and ready to run in `backend/` and `frontend/`.

---

## 2. Prerequisites (install once)

```bash
# 1. PostgreSQL + pgvector extension
#    macOS:   brew install postgresql pgvector
#    Ubuntu:  sudo apt install postgresql postgresql-contrib
#             then build/install pgvector: https://github.com/pgvector/pgvector#installation

# 2. Ollama
#    Download from https://ollama.com/download, then:
ollama pull qwen3:8b
ollama run qwen3:8b "hello"        # confirm it responds

# 3. Tesseract OCR
#    macOS:   brew install tesseract
#    Ubuntu:  sudo apt install tesseract-ocr

# 4. Python 3.11+ and Node.js 18+
python3 --version
node --version
```

---

## 3. Database setup

```bash
# Create the database and user
psql postgres -c "CREATE DATABASE saledeed_db;"
psql postgres -c "CREATE USER saledeed_user WITH PASSWORD 'password';"
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE saledeed_db TO saledeed_user;"

# Enable the vector extension INSIDE that database
psql saledeed_db -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

---

## 4. Backend setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# edit .env if your DB password / Ollama host differ from the defaults

python app.py
# -> Flask runs on http://localhost:5000
# -> db.create_all() creates all tables automatically on first run
```

**Test it's alive:** `curl http://localhost:5000/api/health` → `{"status": "ok"}`

---

## 5. Frontend setup

```bash
cd frontend
npm install
npm run dev
# -> Vite runs on http://localhost:5173 and proxies /api to the Flask backend
```

Open **http://localhost:5173** — register an account, upload a Sales Deed
PDF (≤10 MB), and it will run through the full pipeline: extraction → OCR
(if needed) → chunking → embeddings → RAG → extraction agent → verification
→ risk analysis → risk resolution → translation (if Tamil selected) → report.

---

## 6. Making yourself an admin (optional)

Registration always creates a `user` role. To promote yourself to `admin`
(to see every user's documents on `/admin`):

```bash
psql saledeed_db -c "UPDATE users SET role='admin' WHERE email='you@example.com';"
```

---

## 7. Project structure

```
sales-deed-ai/
├── backend/
│   ├── app.py                 # thin Flask entrypoint — wires blueprints only
│   ├── config.py               # env-driven configuration
│   ├── extensions.py           # shared db / jwt / cors instances
│   ├── models/                 # SQLAlchemy models (users, documents, chunks, analysis...)
│   ├── routes/                 # auth, document, analysis, report blueprints
│   ├── services/                # pdf, ocr, chunking, embedding, rag, ollama, report
│   ├── agents/                  # the 7 specialized agents (Modules 3, 6-12, 16)
│   ├── graph/                   # LangGraph state, nodes, workflow (Modules 13-15)
│   ├── prompts/                 # system prompts per agent
│   └── utils/                   # validators, security, logger
└── frontend/
    └── src/
        ├── pages/                # Landing, Login, Register, Dashboard, Upload,
        │                         # Documents, Analysis, History, Profile, Admin
        ├── components/           # RiskBadge, EvidenceModal, ProcessTimeline,
        │                         # LanguageSwitcher, HeroSeal
        ├── layouts/               # DashboardLayout (sidebar + topbar)
        ├── context/               # AuthContext, LanguageContext
        └── services/              # api.js, documents.js
```

---

## 8. What's fully working vs. what to harden further

**Fully implemented and runnable:**
- Auth (register/login/JWT/roles), PDF upload + validation (10 MB, PDF-only,
  corrupted-file rejection), PDF text extraction, OCR fallback, text cleaning,
  section-aware chunking, pgvector embedding storage + cosine-similarity
  retrieval, the full LangGraph pipeline with a conditional risk branch,
  every one of the 7 agents wired to Qwen3 8B via Ollama, structured JSON
  schema enforcement, evidence-linked verification, bilingual UI with a
  protected-key translation guard, and the full React frontend.

**Recommended next hardening steps** (call these out to whoever continues
building this, per the "explain every phase" instruction in the original
spec):
1. Add Alembic migrations instead of `db.create_all()` for production.
2. Add rate limiting / request size logging on the upload endpoint.
3. Add a PDF export of the report (currently downloads as JSON) — the `pdf`
   generation library of your choice (e.g. `fpdf2` or `reportlab`) slots into
   `services/report_service.py`.
4. Add a token blocklist table if you need true server-side JWT logout.
5. Tamil OCR (`tesseract --list-langs` → install `tam.traineddata`) for
   scanned Tamil-language deeds — hook point is `services/ocr_service.py`.
6. Add automated tests around `utils/validators.py` and the LangGraph
   conditional edges.

---

## 9. Troubleshooting

| Symptom | Likely cause |
|---|---|
| `psycopg2.OperationalError` on startup | Postgres isn't running, or `DATABASE_URL` in `.env` is wrong |
| `ollama.ResponseError: model not found` | Run `ollama pull qwen3:8b` |
| Upload succeeds but analysis hangs | Check `ollama run qwen3:8b` responds directly first — first inference call can be slow while the model loads into memory |
| OCR returns empty text | Confirm `tesseract --version` works, and `TESSERACT_CMD` in `.env` points to the right binary |
| Frontend shows "Could not reach the backend" | Flask isn't running on port 5000, or `vite.config.js` proxy target doesn't match |
