from app.core.exceptions import AuthenticationError


class StubGitHubClient:
    async def close(self) -> None:
        return None

    async def list_repositories(self, owner=None, owner_type=None):
        return [
            {
                "id": 1,
                "name": "connector",
                "full_name": "demo/connector",
                "private": False,
                "html_url": "https://github.com/demo/connector",
                "description": "Demo repo",
            }
        ]

    async def list_issues(self, owner, repo, state="open", per_page=30):
        return [
            {
                "number": 42,
                "title": "Bug report",
                "state": state,
                "user": "octocat",
                "created_at": "2026-03-28T00:00:00Z",
                "html_url": f"https://github.com/{owner}/{repo}/issues/42",
                "body": "Description: Demo knowledge base\nVector Store: Qdrant\nEmbedding Model: text-embedding-ada-002",
            }
        ]

    async def create_issue(self, owner, repo, title, body=None):
        return {
            "number": 99,
            "title": title,
            "state": "open",
            "user": "octocat",
            "created_at": "2026-03-28T00:00:00Z",
            "html_url": f"https://github.com/{owner}/{repo}/issues/99",
            "body": body,
        }


class FailingGitHubClient(StubGitHubClient):
    async def list_repositories(self, owner=None, owner_type=None):
        raise AuthenticationError()


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "github-cloud-connector"}


def test_list_repositories_endpoint(client, override_github_client):
    async def dependency_override():
        yield StubGitHubClient()

    override_github_client(dependency_override)
    response = client.get("/repos")

    assert response.status_code == 200
    assert response.json()[0]["full_name"] == "demo/connector"


def test_list_issues_endpoint(client, override_github_client):
    async def dependency_override():
        yield StubGitHubClient()

    override_github_client(dependency_override)
    response = client.get("/repos/demo/connector/issues", params={"state": "open", "per_page": 10})

    assert response.status_code == 200
    assert response.json()[0]["number"] == 42


def test_create_issue_endpoint(client, override_github_client):
    async def dependency_override():
        yield StubGitHubClient()

    override_github_client(dependency_override)
    response = client.post("/repos/demo/connector/issues", json={"title": "New issue", "body": "Please fix."})

    assert response.status_code == 201
    assert response.json()["title"] == "New issue"


def test_create_issue_rejects_blank_title(client, override_github_client):
    async def dependency_override():
        yield StubGitHubClient()

    override_github_client(dependency_override)
    response = client.post("/repos/demo/connector/issues", json={"title": "   ", "body": "Nope"})

    assert response.status_code == 422
    assert response.json()["error"] == "validation_error"


def test_list_knowledge_bases_endpoint(client, override_github_client):
    async def dependency_override():
        yield StubGitHubClient()

    override_github_client(dependency_override)
    response = client.get("/knowledge-bases")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Bug report"
    assert response.json()[0]["vector_store"] == "Qdrant"


def test_create_knowledge_base_endpoint(client, override_github_client):
    async def dependency_override():
        yield StubGitHubClient()

    override_github_client(dependency_override)
    response = client.post(
        "/knowledge-bases",
        json={
            "name": "Test",
            "description": "KB description",
            "vector_store": "Qdrant",
            "embedding_model": "text-embedding-ada-002",
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test"
    assert response.json()["embedding_model"] == "text-embedding-ada-002"


def test_api_maps_service_errors(client, override_github_client):
    async def dependency_override():
        yield FailingGitHubClient()

    override_github_client(dependency_override)
    response = client.get("/repos")

    assert response.status_code == 401
    assert response.json()["error"] == "auth_error"
