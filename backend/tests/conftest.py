import os

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_github_client
from app.core.config import get_settings
from app.main import create_app


os.environ.setdefault("GITHUB_TOKEN", "test-token")
os.environ.setdefault("KNOWLEDGE_BASE_REPO_OWNER", "demo")
os.environ.setdefault("KNOWLEDGE_BASE_REPO_NAME", "connector")
get_settings.cache_clear()


@pytest.fixture
def app():
    get_settings.cache_clear()
    return create_app()


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def override_github_client(app):
    def _set(client_override):
        app.dependency_overrides[get_github_client] = client_override

    yield _set
    app.dependency_overrides.clear()
