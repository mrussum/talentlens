# TalentLens

AI-powered candidate assessment report generator. A talent assessor pastes raw
interview notes; Claude returns a standardised, professional candidate report
with strengths, development areas, role-fit score, evidence-backed competency
ratings, and tailored STAR follow-up questions.

- **Frontend** — React 18 + TypeScript + Vite
- **Backend** — Python 3.11 + FastAPI + Uvicorn
- **AI** — Anthropic Claude API (`claude-sonnet-4-20250514` by default)
- **Validation** — Pydantic v2
- **Infra** — Docker + docker-compose

## Quick start

```bash
cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY
docker compose up --build
```

Then open <http://localhost:5173>.

The backend exposes an API on <http://localhost:8000> with interactive docs at
<http://localhost:8000/docs>.

## Local development (without Docker)

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
ANTHROPIC_API_KEY=sk-ant-... uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Vite's dev server proxies `/api/*` to <http://localhost:8000>, so no extra
config is needed.

## API

| Method | Path                 | Body                                                   | Returns |
|-------:|----------------------|--------------------------------------------------------|---------|
| `GET`  | `/api/health`        | —                                                      | `{ status, version }` |
| `GET`  | `/api/frameworks`    | —                                                      | available competency frameworks |
| `POST` | `/api/generate`      | `{ notes, role?, competency_framework? }`              | `GenerateResponse` envelope |

Every response uses the `GenerateResponse` envelope:

```json
{ "success": true, "data": { ... CandidateReport ... }, "latency_ms": 4123 }
```

On failure `success` is `false` and `error` is populated; `latency_ms` is
always present.

## Competency frameworks

Frameworks are loaded at runtime from `backend/app/config/competencies.json`.
Two are bundled — `saville_wave` (default) and `general`. Add a new framework
by adding a top-level key with `label` and `competencies[]` — no code change
required.

## Sample scenarios

The frontend ships three quick-start scenarios — Senior Product Manager,
Graduate Analyst, Sales Director — pre-loaded with realistic 300–400 word
interview notes. The same fixtures live in `backend/app/config/samples.py` so
backend tests can exercise the same inputs.

## Prompt builder verification (offline)

```bash
cd backend
python tests/test_prompt_builder.py
```

This checks the rendered prompt for each sample without calling the API:
mandatory raw-JSON opener, framework + role + notes embedding, all 12 Saville
Wave competencies present.

## Operational notes

- `ANTHROPIC_API_KEY` is server-side only. It is never bundled into the
  frontend build and `.env` is git-ignored.
- Notes are sanitised before being sent to Claude (control-char strip,
  prompt-injection marker defang).
- Every `/api/generate` call emits a structured JSON log line containing
  `timestamp`, `endpoint`, `latency_ms`, `prompt_version`, `competency_count`,
  `fit_score`, `framework`, `model`, `parse_strategy`.
- The Claude response is parsed defensively: `json.loads` → strip markdown
  fences → regex-extract first `{…}` block → return a structured error.
- p95 target latency: < 5 s.

## Project structure

```
talentlens/
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── src/
│       ├── App.tsx
│       ├── main.tsx
│       ├── index.css
│       ├── components/
│       │   ├── InputPanel.tsx
│       │   ├── ReportPanel.tsx
│       │   ├── ScoreMeter.tsx
│       │   ├── CompetencyCard.tsx
│       │   ├── QuestionList.tsx
│       │   └── ExportPanel.tsx
│       ├── hooks/useGenerate.ts
│       └── types/
│           ├── candidate.ts
│           └── samples.ts
├── backend/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/generate.py
│   │   ├── services/claude_service.py
│   │   ├── models/candidate.py
│   │   ├── config/
│   │   │   ├── competencies.json
│   │   │   ├── frameworks.py
│   │   │   └── samples.py
│   │   └── utils/
│   │       ├── prompt_builder.py
│   │       ├── sanitise.py
│   │       └── logging.py
│   └── tests/test_prompt_builder.py
├── docker-compose.yml
├── .env.example
└── README.md
```
