# AI Job Matching & Skill Gap Analyzer

This repository contains a React frontend and a Flask backend for an AI-powered job matching system.

Quick overview
- Frontend: `job-matching-frontend` (Vite + React + Tailwind)
- Backend: `app/` (Flask REST API)
- Data store: `data/jobs.json` (simple JSON file for demo)

Prerequisites
- Node.js >= 22.12.0 (or >= 20.19)
- Python 3.10+

Frontend setup
```bash
cd job-matching-frontend
npm install
npm run dev
```
If `npm install` fails with peer dependency errors, try:
```bash
npm install --legacy-peer-deps
```

Backend setup
```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r app/requirements.txt
# download spaCy model (required for improved skill extraction)
python -m spacy download en_core_web_sm
# run the Flask app
python -m app.run
```

API endpoints (backend)
- `POST /api/jobs` — add a job (JSON: `{ title, description }`)
- `POST /api/upload` — upload resume file (form-data `file`)
- `POST /api/match` — match resume text to stored jobs (JSON: `{ text }`)
- `POST /api/analyze` — extract skills and detect gaps (JSON: `{ text, job_id?|job_description? }`)

- `POST /api/chat` — proxy to configured LLM provider. JSON body is forwarded to `LLM_API_URL`.

Notes
- The backend uses simple TF-IDF + cosine similarity for matching as a starter.
- Skill extraction uses a small vocabulary with a spaCy-based enhancement when `spacy` and the `en_core_web_sm` model are available.
- For production use, replace `data/jobs.json` with a real database and replace TF-IDF with embeddings (BERT) for better accuracy.

Next tasks you can ask me to do
- Upgrade the frontend Tailwind/PostCSS setup and resolve Vite errors.
- Add Dockerfiles for frontend & backend.
- Improve NLP pipeline: add transformers-based embeddings and persistent models.
- Add unit/integration tests and a CI workflow.

LLM / Chatbot setup
1. Create a `.env` file next to the repository root (do NOT commit it).
2. Add your provider info there, for example:

```
LLM_API_URL=https://api.your-llm.com/v1/generate
LLM_API_KEY=sk-xxxx
```

3. Run the backend so the `/api/chat` endpoint can forward requests to your LLM provider.

Author

Abdullah Zuhry
GitHub: https://github.com/Abdullahsuhry
