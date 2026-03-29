from pydantic import BaseModel, ConfigDict, field_validator


class CreateIssueRequest(BaseModel):
    title: str
    body: str | None = None

    model_config = ConfigDict(str_strip_whitespace=True)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Issue title must not be empty.")
        return value

    @field_validator("body")
    @classmethod
    def normalize_body(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class CreateKnowledgeBaseRequest(BaseModel):
    name: str
    description: str | None = None
    vector_store: str
    embedding_model: str

    model_config = ConfigDict(str_strip_whitespace=True)

    @field_validator("name", "vector_store", "embedding_model")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field must not be empty.")
        return value

    @field_validator("description")
    @classmethod
    def normalize_description(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None
