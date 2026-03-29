from typing import Any, Literal

import httpx

from app.core.config import Settings
from app.core.exceptions import (
    AuthenticationError,
    NotFoundError,
    UpstreamServiceError,
    UpstreamTimeoutError,
    UpstreamValidationError,
)


class GitHubClient:
    def __init__(self, settings: Settings, transport: httpx.AsyncBaseTransport | None = None) -> None:
        self._settings = settings
        token = settings.require_github_token()
        self._client = httpx.AsyncClient(
            base_url=settings.github_api_base_url.rstrip("/"),
            timeout=settings.request_timeout_seconds,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            transport=transport,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def list_repositories(
        self,
        owner: str | None = None,
        owner_type: Literal["user", "org"] | None = None,
    ) -> list[dict[str, Any]]:
        if owner and owner_type == "org":
            data = await self._request("GET", f"/orgs/{owner}/repos")
        elif owner:
            data = await self._request("GET", f"/users/{owner}/repos")
        else:
            data = await self._request("GET", "/user/repos")

        return [self._normalize_repo(repo) for repo in data]

    async def list_issues(
        self,
        owner: str,
        repo: str,
        state: Literal["open", "closed", "all"] = "open",
        per_page: int = 30,
    ) -> list[dict[str, Any]]:
        data = await self._request(
            "GET",
            f"/repos/{owner}/{repo}/issues",
            params={"state": state, "per_page": per_page},
        )
        return [self._normalize_issue(issue) for issue in data if "pull_request" not in issue]

    async def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str | None = None,
    ) -> dict[str, Any]:
        if not title.strip():
            raise UpstreamValidationError("Issue title must not be empty.")

        payload: dict[str, Any] = {"title": title.strip()}
        if body is not None:
            payload["body"] = body

        data = await self._request("POST", f"/repos/{owner}/{repo}/issues", json=payload)
        return self._normalize_issue(data)

    async def _request(self, method: str, url: str, **kwargs: Any) -> Any:
        try:
            response = await self._client.request(method, url, **kwargs)
        except httpx.TimeoutException as exc:
            raise UpstreamTimeoutError() from exc
        except httpx.HTTPError as exc:
            raise UpstreamServiceError("Failed to connect to GitHub.") from exc

        if response.status_code in (401, 403):
            raise AuthenticationError()
        if response.status_code == 404:
            raise NotFoundError()
        if response.status_code == 422:
            detail = self._extract_message(response)
            raise UpstreamValidationError(detail)
        if response.status_code >= 500:
            raise UpstreamServiceError("GitHub returned a server-side error.")
        if response.is_error:
            detail = self._extract_message(response)
            raise UpstreamServiceError(detail)

        return response.json()

    @staticmethod
    def _extract_message(response: httpx.Response) -> str:
        try:
            payload = response.json()
        except ValueError:
            return "GitHub returned an invalid response."
        return payload.get("message", "GitHub request failed.")

    @staticmethod
    def _normalize_repo(repo: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": repo["id"],
            "name": repo["name"],
            "full_name": repo["full_name"],
            "private": repo["private"],
            "html_url": repo["html_url"],
            "description": repo.get("description"),
        }

    @staticmethod
    def _normalize_issue(issue: dict[str, Any]) -> dict[str, Any]:
        user = issue.get("user") or {}
        return {
            "number": issue["number"],
            "title": issue["title"],
            "state": issue["state"],
            "user": user.get("login", "unknown"),
            "created_at": issue["created_at"],
            "html_url": issue["html_url"],
            "body": issue.get("body"),
        }
