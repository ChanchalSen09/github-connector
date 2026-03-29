# Assignment Workspace

This repo now contains both assignments:

- [backend](d:\Code\Project\Github Connector\backend): FastAPI GitHub cloud connector
- [frontend](d:\Code\Project\Github Connector\frontend): React + Tailwind knowledge base UI

## Full flow setup

### 1. Configure backend env

Create `backend/.env` from `backend/.env.example` and set:

```env
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_API_BASE_URL=https://api.github.com
APP_ENV=development
FRONTEND_ORIGIN=http://localhost:5173
KNOWLEDGE_BASE_REPO_OWNER=your-github-username-or-org
KNOWLEDGE_BASE_REPO_NAME=your-target-repository
```

The knowledge base UI stores entries as GitHub issues in the configured repository.

### 2. Configure frontend env

Create `frontend/.env` from `frontend/.env.example` and set:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Backend

Start in `backend/`:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

Run tests:

```bash
cd backend
python -m pytest
```

## Frontend

Start in `frontend/`:

```bash
cd frontend
npm install
npm run dev
```

Build:

```bash
cd frontend
npm run build
```

## Notes

- The frontend now uses the backend API for list and create flows.
- The `Create New` drawer submits to the backend and refreshes the card grid immediately.
- Search is handled client-side over the fetched knowledge base entries.
- The current UI is matched closely to the screenshots and uses GitHub issues as its backing store.
