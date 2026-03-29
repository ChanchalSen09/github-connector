from collections.abc import AsyncGenerator

from app.core.config import get_settings
from app.services.github_client import GitHubClient


async def get_github_client() -> AsyncGenerator[GitHubClient, None]:
    settings = get_settings()
    client = GitHubClient(settings=settings)
    try:
        yield client
    finally:
        await client.close()
