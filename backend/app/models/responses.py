from typing import Any

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class RepoResponse(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    html_url: str
    description: str | None = None


class IssueResponse(BaseModel):
    number: int
    title: str
    state: str
    user: str
    created_at: str
    html_url: str
    body: str | None = None


class KnowledgeBaseResponse(BaseModel):
    id: int
    name: str
    description: str
    vector_store: str
    embedding_model: str
    created_on: str
    html_url: str


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Any | None = None
