# College Documentation Outline

## Abstract
Resumate AI is a local NLP application that analyzes resume/job-description alignment using document extraction, skill matching, keyword overlap, vector similarity, and transparent scoring.

## Introduction and problem statement
Students need role-specific feedback, while manual review is slow and inconsistent. The system turns resume text and a target role into an explainable report.

## Objectives and scope
Extract resume text, detect sections and skills, compare job terms, calculate an ATS-style compatibility estimate, recommend truthful improvements, persist history, and generate a report. It is intended for student and early-career analysis, not recruitment decisions.

## Existing and proposed system
Existing tools often hide their scoring logic or require paid services. The proposed system is local, modular, and transparent about evidence and limitations.

## Requirements
Functional requirements include upload, validation, analysis, history, deletion, and PDF export. Non-functional requirements include responsive layout, privacy-conscious local storage, understandable modules, and graceful errors. A normal student laptop, macOS/Linux, Python 3.10+, Node.js 18+, and internet only for initial package installation are sufficient.

## Architecture and data flow
User -> React client -> Flask API -> parser -> NLP preprocessing -> skill/keyword extraction -> vector similarity -> scoring -> insight generation -> SQLite/report -> result dashboard.

## Modules
`resume_parser.py` handles PDF/DOCX input. `nlp.py` detects sections, skills, keywords, and similarity. `scoring.py` applies weighted rules. `analyzer.py` assembles evidence-backed insights. `database.py` persists structured results. `report.py` creates a PDF.

## Database and API design
SQLite stores analysis id, role, score, date, and structured JSON. REST routes are documented in the README.

## Testing, results, limitations, future scope
Use TEST_CASES.md for the test plan and `backend/test_backend.py` for automated checks. Results are data-dependent, not hard-coded. OCR, multilingual support, stronger transformer embeddings, authentication, and richer entity extraction are suitable future improvements.

## Conclusion and references
The project demonstrates practical NLP and explainable scoring with technologies appropriate for a B.Tech CSE project. References: Flask documentation, PyMuPDF documentation, python-docx documentation, scikit-learn user guide, ReportLab documentation.
