# GitHub Cloud Connector

A FastAPI backend that authenticates with GitHub using a Personal Access Token and exposes repository, issue, and knowledge-base workflows.

## Setup

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set:

```env
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_API_BASE_URL=https://api.github.com
APP_ENV=development
FRONTEND_ORIGIN=http://localhost:5173
KNOWLEDGE_BASE_REPO_OWNER=your-github-username-or-org
KNOWLEDGE_BASE_REPO_NAME=your-target-repository
```

## Run

```bash
python -m uvicorn app.main:app --reload
```

## Test

```bash
python -m pytest
```

## Endpoints

- `GET /health`
- `GET /repos`
- `GET /repos/{owner}/{repo}/issues`
- `POST /repos/{owner}/{repo}/issues`
- `GET /knowledge-bases`
- `POST /knowledge-bases`

## Knowledge base flow

The UI-facing knowledge base endpoints map to GitHub issues in the configured repository:

- `GET /knowledge-bases` lists open issues and transforms them into UI cards
- `POST /knowledge-bases` creates a new GitHub issue using the knowledge base form data
