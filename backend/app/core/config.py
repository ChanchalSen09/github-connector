from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.exceptions import ConfigurationError


class Settings(BaseSettings):
    github_token: str | None = Field(default=None, alias="GITHUB_TOKEN")
    github_api_base_url: str = Field(default="https://api.github.com", alias="GITHUB_API_BASE_URL")
    app_env: str = Field(default="development", alias="APP_ENV")
    request_timeout_seconds: float = 15.0
    frontend_origin: str = Field(default="http://localhost:5173", alias="FRONTEND_ORIGIN")
    knowledge_base_repo_owner: str | None = Field(default=None, alias="KNOWLEDGE_BASE_REPO_OWNER")
    knowledge_base_repo_name: str | None = Field(default=None, alias="KNOWLEDGE_BASE_REPO_NAME")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def require_github_token(self) -> str:
        token = (self.github_token or "").strip()
        if not token:
            raise ConfigurationError(
                message="GitHub token is not configured. Set GITHUB_TOKEN in your environment or .env file."
            )
        return token

    def require_knowledge_base_repo(self) -> tuple[str, str]:
        owner = (self.knowledge_base_repo_owner or "").strip()
        repo = (self.knowledge_base_repo_name or "").strip()

        if not owner or not repo:
            raise ConfigurationError(
                message=(
                    "Knowledge base repository is not configured. Set KNOWLEDGE_BASE_REPO_OWNER and "
                    "KNOWLEDGE_BASE_REPO_NAME in your environment or .env file."
                )
            )

        return owner, repo


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
