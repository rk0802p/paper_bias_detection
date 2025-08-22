

## Project Overview

Research Paper Plagiarism & Similarity Analysis is a web tool that reads an academic paper (PDF), extracts the main sections — Title, Abstract, Methodology, and Conclusions — and evaluates how similar each section is to related, previously published work. Results are shown as section‑wise similarity percentages with categorized levels and direct links to the closest matching sources.

### What it does
- Extracts text from uploaded PDFs (with robust fallbacks for tricky layouts)
- Splits content into four sections: Title, Abstract, Methodology, Conclusions
- Finds potentially similar papers using public scholarly APIs (Semantic Scholar and OpenAlex)
- Computes TF‑IDF cosine similarity to estimate overlap
- Classifies similarity levels:
  - 1–25%: Low similarity (mostly original ideas)
  - 25–50%: Moderate similarity
  - >50%: High similarity (heavily copied)
- Displays top matching sources with links for each section

### How it works (pipeline)
1) PDF ingestion: `pdfplumber` extracts text; if spacing is broken, the app reconstructs text from word boxes.
2) Sectioning: simple, robust regex heuristics isolate Title/Abstract/Methodology/Conclusions.
3) Retrieval: builds multiple concise queries per section and calls Semantic Scholar and OpenAlex; results are de‑duplicated.
4) Scoring: TF‑IDF vectorization and cosine similarity produce a percent score per match; the best score per section drives the displayed category.
5) Reporting: overall similarity is a weighted average favoring Abstract and Methodology; the UI renders per‑section tables with match percentage, title, and link.

### Tech stack
- Backend: Python, FastAPI, pdfplumber, scikit‑learn, requests
- Frontend: React (Vite), Axios

---

## Repository Layout
```
backend/
  api.py                 # FastAPI server, exposes POST /analyze
  requirements.txt       # Backend dependencies
  src/
    plagiarism_checker.py  # Section extraction, retrieval, similarity, reporting
web/
  index.html            # Paper texture theme
  src/ui/App.tsx        # React UI
  vite.config.ts        # Dev server proxy to backend
```

---

## Requirements

### Backend
- Python 3.10+
- Packages (installed via `backend/requirements.txt`):
  - fastapi, uvicorn, pdfplumber, numpy, scikit‑learn, requests, scipy

### Frontend
- Node.js 18+ and npm (or pnpm/yarn)

---

## Setup & Run

1) Clone and open this repository.

2) Start the backend API
```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```
The API will be available at `http://localhost:8000`.

3) Start the frontend
```bash
cd web
npm install
npm run dev
# open http://localhost:5173
```
The frontend proxies API calls to `http://localhost:8000` (configured in `vite.config.ts`). To override, create `web/.env`:
```
VITE_API_BASE=http://localhost:8000
```

---

## Notes & Limitations
- Similarity is an approximate signal intended to aid manual review; it is not a legal plagiarism determination.
- Retrieval quality depends on the public APIs; network availability may affect results.
- For image‑only PDFs, OCR is not currently enabled; add OCR if needed.
