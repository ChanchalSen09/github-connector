import httpx
import pytest

from app.core.config import Settings
from app.core.exceptions import (
    AuthenticationError,
    NotFoundError,
    UpstreamTimeoutError,
    UpstreamValidationError,
)
from app.services.github_client import GitHubClient


def transport_for(handler):
    return httpx.MockTransport(handler)


@pytest.mark.asyncio
async def test_client_sends_auth_header():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer test-token"
        return httpx.Response(
            200,
            json=[
                {
                    "id": 1,
                    "name": "repo",
                    "full_name": "demo/repo",
                    "private": False,
                    "html_url": "https://github.com/demo/repo",
                    "description": None,
                }
            ],
        )

    client = GitHubClient(Settings(GITHUB_TOKEN="test-token"), transport=transport_for(handler))

    repos = await client.list_repositories()
    await client.close()

    assert repos[0]["name"] == "repo"


@pytest.mark.asyncio
async def test_client_maps_401_to_auth_error():
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"message": "Bad credentials"})

    client = GitHubClient(Settings(GITHUB_TOKEN="test-token"), transport=transport_for(handler))

    with pytest.raises(AuthenticationError):
        await client.list_repositories()

    await client.close()


@pytest.mark.asyncio
async def test_client_maps_404_to_not_found():
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"message": "Not Found"})

    client = GitHubClient(Settings(GITHUB_TOKEN="test-token"), transport=transport_for(handler))

    with pytest.raises(NotFoundError):
        await client.list_issues("demo", "missing")

    await client.close()


@pytest.mark.asyncio
async def test_client_maps_422_to_validation_error():
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(422, json={"message": "Validation Failed"})

    client = GitHubClient(Settings(GITHUB_TOKEN="test-token"), transport=transport_for(handler))

    with pytest.raises(UpstreamValidationError, match="Validation Failed"):
        await client.create_issue("demo", "repo", "Valid title")

    await client.close()


@pytest.mark.asyncio
async def test_client_maps_timeout_to_gateway_timeout():
    def handler(_: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timeout")

    client = GitHubClient(Settings(GITHUB_TOKEN="test-token"), transport=transport_for(handler))

    with pytest.raises(UpstreamTimeoutError):
        await client.list_repositories()

    await client.close()


@pytest.mark.asyncio
async def test_list_issues_filters_pull_requests():
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json=[
                {
                    "number": 1,
                    "title": "Issue",
                    "state": "open",
                    "user": {"login": "octocat"},
                    "created_at": "2026-03-28T00:00:00Z",
                    "html_url": "https://github.com/demo/repo/issues/1",
                    "body": "Description: Example",
                },
                {
                    "number": 2,
                    "title": "PR",
                    "state": "open",
                    "user": {"login": "octocat"},
                    "created_at": "2026-03-28T00:00:00Z",
                    "html_url": "https://github.com/demo/repo/pull/2",
                    "pull_request": {},
                },
            ],
        )

    client = GitHubClient(Settings(GITHUB_TOKEN="test-token"), transport=transport_for(handler))

    issues = await client.list_issues("demo", "repo")
    await client.close()

    assert len(issues) == 1
    assert issues[0]["number"] == 1
    assert issues[0]["body"] == "Description: Example"
