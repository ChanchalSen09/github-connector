from datetime import datetime

from fastapi import APIRouter, Depends, status

from app.api.deps import get_github_client
from app.core.config import get_settings
from app.models.requests import CreateKnowledgeBaseRequest
from app.models.responses import KnowledgeBaseResponse
from app.services.github_client import GitHubClient

router = APIRouter(prefix="/knowledge-bases", tags=["knowledge-bases"])

_DESCRIPTION_PREFIX = "Description:"
_VECTOR_STORE_PREFIX = "Vector Store:"
_EMBEDDING_MODEL_PREFIX = "Embedding Model:"


def _serialize_knowledge_base_body(description: str | None, vector_store: str, embedding_model: str) -> str:
    description_text = (description or "").strip() or "No description provided."
    return "\n".join(
        [
            f"{_DESCRIPTION_PREFIX} {description_text}",
            f"{_VECTOR_STORE_PREFIX} {vector_store}",
            f"{_EMBEDDING_MODEL_PREFIX} {embedding_model}",
        ]
    )


def _parse_knowledge_base_body(body: str | None) -> tuple[str, str, str]:
    description = "No description provided."
    vector_store = "Unknown"
    embedding_model = "Unknown"

    for line in (body or "").splitlines():
        if line.startswith(_DESCRIPTION_PREFIX):
            description = line.removeprefix(_DESCRIPTION_PREFIX).strip() or description
        elif line.startswith(_VECTOR_STORE_PREFIX):
            vector_store = line.removeprefix(_VECTOR_STORE_PREFIX).strip() or vector_store
        elif line.startswith(_EMBEDDING_MODEL_PREFIX):
            embedding_model = line.removeprefix(_EMBEDDING_MODEL_PREFIX).strip() or embedding_model

    return description, vector_store, embedding_model


def _to_knowledge_base_response(issue: dict) -> KnowledgeBaseResponse:
    description, vector_store, embedding_model = _parse_knowledge_base_body(issue.get("body"))
    created_on = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00")).strftime("%d/%m/%Y")

    return KnowledgeBaseResponse(
        id=issue["number"],
        name=issue["title"],
        description=description,
        vector_store=vector_store,
        embedding_model=embedding_model,
        created_on=created_on,
        html_url=issue["html_url"],
    )


@router.get("", response_model=list[KnowledgeBaseResponse], summary="List knowledge bases")
async def list_knowledge_bases(
    github_client: GitHubClient = Depends(get_github_client),
) -> list[KnowledgeBaseResponse]:
    owner, repo = get_settings().require_knowledge_base_repo()
    issues = await github_client.list_issues(owner=owner, repo=repo, state="open", per_page=100)
    return [_to_knowledge_base_response(issue) for issue in issues]


@router.post("", response_model=KnowledgeBaseResponse, status_code=status.HTTP_201_CREATED, summary="Create knowledge base")
async def create_knowledge_base(
    payload: CreateKnowledgeBaseRequest,
    github_client: GitHubClient = Depends(get_github_client),
) -> KnowledgeBaseResponse:
    owner, repo = get_settings().require_knowledge_base_repo()
    issue = await github_client.create_issue(
        owner=owner,
        repo=repo,
        title=payload.name,
        body=_serialize_knowledge_base_body(
            description=payload.description,
            vector_store=payload.vector_store,
            embedding_model=payload.embedding_model,
        ),
    )
    return _to_knowledge_base_response(issue)
