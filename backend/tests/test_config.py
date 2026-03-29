import pytest

from app.core.config import Settings
from app.core.exceptions import ConfigurationError


def test_settings_raise_clear_error_when_token_missing():
    settings = Settings(GITHUB_TOKEN="")

    with pytest.raises(ConfigurationError, match="GitHub token is not configured"):
        settings.require_github_token()


def test_settings_raise_clear_error_when_knowledge_base_repo_missing():
    settings = Settings(GITHUB_TOKEN="test-token", KNOWLEDGE_BASE_REPO_OWNER="", KNOWLEDGE_BASE_REPO_NAME="")

    with pytest.raises(ConfigurationError, match="Knowledge base repository is not configured"):
        settings.require_knowledge_base_repo()
