"""Summarisation endpoint."""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.ai_service import generate_summary
from app.services.storage_service import get_document_content

router = APIRouter()
logger = logging.getLogger(__name__)


class SummariseRequest(BaseModel):
    """Request body for summarisation."""

    document_id: str
    s3_key: str


@router.post("/summarise")
async def summarise_document(request: SummariseRequest):
    """Generate an AI summary for an uploaded document."""
    content = get_document_content(request.s3_key)
    if not content:
        raise HTTPException(status_code=404, detail="Document not found.")

    summary = generate_summary(content)

    logger.info(
        "Summary generated | document_id=%s | time=%s",
        request.document_id,
        datetime.now(timezone.utc).isoformat(),
    )

    return {
        "document_id": request.document_id,
        "summary": summary,
    }
