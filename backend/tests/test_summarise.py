"""Tests for the summarise endpoint."""

from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@patch("app.routes.summarise.get_document_content")
def test_summarise_returns_404_for_missing_document(mock_get):
    """Verify summarise returns 404 when document not found."""
    mock_get.return_value = None
    response = client.post(
        "/summarise",
        json={"document_id": "test-id", "s3_key": "documents/missing.txt"},
    )
    assert response.status_code == 404
    assert "Document not found" in response.json()["detail"]


@patch("app.routes.summarise.generate_summary")
@patch("app.routes.summarise.get_document_content")
def test_summarise_returns_summary(mock_get, mock_summary):
    """Verify summarise returns AI-generated summary."""
    mock_get.return_value = "Long document content about governance policies."
    mock_summary.return_value = "This document covers governance policies."
    response = client.post(
        "/summarise",
        json={"document_id": "test-id", "s3_key": "documents/test.txt"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["summary"] == "This document covers governance policies."
    assert data["document_id"] == "test-id"
