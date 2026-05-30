"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Verify service availability."""
    return {"status": "healthy", "service": "AI Governance Assistant"}
