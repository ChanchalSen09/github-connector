from typing import Literal

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_github_client
from app.models.requests import CreateIssueRequest
from app.models.responses import IssueResponse, RepoResponse
from app.services.github_client import GitHubClient

router = APIRouter(tags=["github"])


@router.get("/repos", response_model=list[RepoResponse], summary="List repositories")
async def list_repositories(
    owner: str | None = Query(default=None, min_length=1),
    owner_type: Literal["user", "org"] | None = Query(default=None),
    github_client: GitHubClient = Depends(get_github_client),
) -> list[RepoResponse]:
    repos = await github_client.list_repositories(owner=owner, owner_type=owner_type)
    return [RepoResponse.model_validate(repo) for repo in repos]


@router.get(
    "/repos/{owner}/{repo}/issues",
    response_model=list[IssueResponse],
    summary="List repository issues",
)
async def list_issues(
    owner: str,
    repo: str,
    state: Literal["open", "closed", "all"] = Query(default="open"),
    per_page: int = Query(default=30, ge=1, le=100),
    github_client: GitHubClient = Depends(get_github_client),
) -> list[IssueResponse]:
    issues = await github_client.list_issues(owner=owner, repo=repo, state=state, per_page=per_page)
    return [IssueResponse.model_validate(issue) for issue in issues]


@router.post(
    "/repos/{owner}/{repo}/issues",
    response_model=IssueResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a repository issue",
)
async def create_issue(
    owner: str,
    repo: str,
    payload: CreateIssueRequest,
    github_client: GitHubClient = Depends(get_github_client),
) -> IssueResponse:
    issue = await github_client.create_issue(owner=owner, repo=repo, title=payload.title, body=payload.body)
    return IssueResponse.model_validate(issue)
