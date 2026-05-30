"""Document upload endpoint."""

import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.storage_service import upload_to_s3

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document to S3 storage."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")

    allowed_types = [
        "application/pdf",
        "text/plain",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    document_id = str(uuid.uuid4())
    s3_key = f"documents/{document_id}/{file.filename}"

    content = await file.read()
    upload_to_s3(content, s3_key, file.content_type or "application/octet-stream")

    logger.info(
        "Document uploaded | id=%s | filename=%s | size=%d | time=%s",
        document_id,
        file.filename,
        len(content),
        datetime.now(timezone.utc).isoformat(),
    )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "s3_key": s3_key,
        "message": "Document uploaded successfully.",
    }
