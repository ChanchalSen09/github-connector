from fastapi import APIRouter

from app.models.responses import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="github-cloud-connector")
