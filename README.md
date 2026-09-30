# AIR2DNA

An evidence-bounded computational biology experience for tracing air-pollution exposure through *modeled* molecular mechanisms. It is educational and research-oriented, not a diagnostic or personal mutation-risk predictor.

## Run locally

```powershell
# API
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000

# Web app (separate terminal)
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`. The frontend runs without the API using its local scenario data; configure `NEXT_PUBLIC_API_URL` to use the FastAPI service. In Vercel production, leave it unset: the frontend calls the same-origin `/api` rewrite.

## Vercel services

The root [vercel.json](vercel.json) defines two services in one Vercel project: `frontend` (public at `/`) and `backend` (public only through `/api/*`). The browser calls `/api` on the shared domain, so there is no browser-visible backend hostname and no service binding. Set `DATA_GOV_SG_API_KEY` as a Vercel environment variable for the backend service only; do not set `NEXT_PUBLIC_API_URL` in Vercel. Run `vercel dev` to exercise the services together locally.

## Live Singapore PM2.5

Copy `backend/.env.example` to `backend/.env`, then add a data.gov.sg API key as `DATA_GOV_SG_API_KEY`. The key stays on the FastAPI server; the browser calls `GET /api/air-quality/latest` and never receives it. In the scenario builder, select **Use latest NEA reading** to load the central-region PM2.5 reading. If the key or upstream API is unavailable, the fixed haze-demo value remains usable and is clearly labeled as a demo.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for boundaries, evidence policy, and limitations.
