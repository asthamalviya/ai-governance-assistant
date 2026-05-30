"""Question-answering endpoint."""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.ai_service import ask_question
from app.services.storage_service import get_document_content

router = APIRouter()
logger = logging.getLogger(__name__)


class AskRequest(BaseModel):
    """Request body for asking a question."""

    document_id: str
    s3_key: str
    question: str


@router.post("/ask")
async def ask_about_document(request: AskRequest):
    """Ask a contextual question about an uploaded document."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    content = get_document_content(request.s3_key)
    if not content:
        raise HTTPException(status_code=404, detail="Document not found.")

    answer = ask_question(content, request.question)

    logger.info(
        "Question answered | document_id=%s | question=%s | time=%s",
        request.document_id,
        request.question[:50],
        datetime.now(timezone.utc).isoformat(),
    )

    return {
        "document_id": request.document_id,
        "question": request.question,
        "answer": answer,
    }
