from fastapi import APIRouter
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health_check() -> dict:
    """
    Health check endpoint to verify API is running
    """
    return {"status": "ok"}
