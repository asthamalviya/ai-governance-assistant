"""Tests for the ask endpoint — input validation and error handling."""

from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ask_rejects_empty_question():
    """Verify ask endpoint rejects empty questions."""
    response = client.post(
        "/ask",
        json={"document_id": "test-id", "s3_key": "documents/test.txt", "question": "   "},
    )
    assert response.status_code == 400
    assert "Question cannot be empty" in response.json()["detail"]


@patch("app.routes.ask.get_document_content")
def test_ask_returns_404_for_missing_document(mock_get):
    """Verify ask endpoint returns 404 when document not found in S3."""
    mock_get.return_value = None
    response = client.post(
        "/ask",
        json={
            "document_id": "test-id",
            "s3_key": "documents/nonexistent.txt",
            "question": "What is this about?",
        },
    )
    assert response.status_code == 404
    assert "Document not found" in response.json()["detail"]


@patch("app.routes.ask.ask_question")
@patch("app.routes.ask.get_document_content")
def test_ask_returns_answer(mock_get, mock_ask):
    """Verify ask endpoint returns AI-generated answer."""
    mock_get.return_value = "This is a document about cloud computing."
    mock_ask.return_value = "The document is about cloud computing."
    response = client.post(
        "/ask",
        json={
            "document_id": "test-id",
            "s3_key": "documents/test.txt",
            "question": "What is this about?",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "The document is about cloud computing."
    assert data["question"] == "What is this about?"
