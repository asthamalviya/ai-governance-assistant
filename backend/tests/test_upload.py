"""Tests for the upload endpoint — input validation."""

from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_rejects_no_file():
    """Verify upload rejects requests without a file."""
    response = client.post("/upload")
    assert response.status_code == 422


def test_upload_rejects_unsupported_type():
    """Verify upload rejects unsupported file types."""
    response = client.post(
        "/upload",
        files={"file": ("malware.exe", b"malicious content", "application/x-msdownload")},
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


@patch("app.routes.upload.upload_to_s3")
def test_upload_accepts_text_file(mock_upload):
    """Verify upload accepts valid text files and returns expected response."""
    mock_upload.return_value = None
    response = client.post(
        "/upload",
        files={"file": ("document.txt", b"Hello world content", "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "document.txt"
    assert "document_id" in data
    assert "s3_key" in data
    assert data["message"] == "Document uploaded successfully."


@patch("app.routes.upload.upload_to_s3")
def test_upload_accepts_pdf(mock_upload):
    """Verify upload accepts PDF files."""
    mock_upload.return_value = None
    response = client.post(
        "/upload",
        files={"file": ("report.pdf", b"%PDF-1.4 content", "application/pdf")},
    )
    assert response.status_code == 200
    assert response.json()["filename"] == "report.pdf"
