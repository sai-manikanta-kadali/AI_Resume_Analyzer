# RESUMATE AI

Resumate AI is a local, explainable resume intelligence and job-match analyzer. Upload a PDF or DOCX resume, paste a target job description, and receive evidence-based matching, skill gaps, section detection, recommendations, local history, and a downloadable PDF report.

## Features

- Real PDF and DOCX text extraction with PyMuPDF and python-docx
- Extensible categorized skill catalog
- Resume section detection and completeness scoring
- Keyword overlap and TF-IDF cosine semantic similarity
- Explainable ATS-style score: skills 40%, keywords 25%, semantic similarity 20%, completeness 10%, formatting 5%
- SQLite analysis history and report generation
- Responsive React interface with a labeled demo mode

## Architecture

`React + Vite` -> `Flask REST API` -> `resume_parser.py` -> `nlp.py` -> `scoring.py` -> `analyzer.py` -> `SQLite/report.py`

The demo endpoint bypasses file decoding only for the provided sample text; it still uses the same analysis, scoring, persistence, and report pipeline.

## Requirements

- macOS or Linux
- Python 3.10+; Python 3.10 is recommended on this macOS setup
- Node.js 18+

## Run locally

```bash
cd "AI_resume Analyzer"
python3.10 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
python backend/app.py
```

Use `python3.10` instead of `python3.13` if your Homebrew Python 3.13 reports an `ensurepip`, `pyexpat`, or `platform.mac_ver()` error.

The core setup uses local TF-IDF cosine similarity and does not download PyTorch. To enable the optional `all-MiniLM-L6-v2` sentence-transformer path, install `backend/requirements-ai.txt` afterward. The application automatically falls back to TF-IDF if that model is unavailable.

In another terminal:

```bash
cd "AI_resume Analyzer/frontend"
npm install
npm run dev
```

Open `http://localhost:5173`. The API health check is `http://localhost:5000/`.

## API

- `GET /` health check
- `POST /api/analyze` multipart fields: `resume`, `job_description`
- `POST /api/demo` JSON fields: `resume_text`, `job_description`
- `POST /api/report` JSON analysis object
- `GET /api/history`
- `GET /api/history/<id>`
- `DELETE /api/history/<id>`

## NLP methodology

Documents are decoded, whitespace-normalized, and scanned for sections, skills, and job terms. TF-IDF converts the resume and job description into vectors; cosine similarity produces the semantic component. Skill and section rules remain visible so the result can be defended in a viva. A future production upgrade can replace the vectorizer with a locally cached sentence-transformers model while preserving the same scoring contract.

## Database

SQLite stores only analysis metadata and structured result JSON: id, target role, score, date, and payload. Raw resume text is not stored.

## Testing

```bash
python3 -m py_compile backend/*.py
python3 -m unittest discover -s backend -p 'test_*.py'
cd frontend && npm run build
```

Manual cases are documented in [TEST_CASES.md](TEST_CASES.md).

## Limitations and future scope

The parser is strongest on text-based documents and may miss content in image-only resumes, unusual layouts, synonyms outside the catalog, or skills represented only by graphics. Future work can add OCR, a local sentence-transformers model, richer project/experience extraction, authentication, and comparative dashboards.
