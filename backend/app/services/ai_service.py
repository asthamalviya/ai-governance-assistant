"""AI service for summarisation and question-answering using OpenAI."""

import logging
from typing import Optional

from openai import OpenAI

from app.utils.config import settings

logger = logging.getLogger(__name__)

_client: Optional[OpenAI] = None


def _get_client() -> OpenAI:
    """Lazy-initialise the OpenAI client."""
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


def generate_summary(document_content: str) -> str:
    """Generate an AI summary of the given document content."""
    try:
        response = _get_client().chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that summarises "
                        "organisational documents clearly and concisely."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Summarise the following document:\n\n{document_content}",
                },
            ],
            max_tokens=500,
            temperature=0.3,
        )
        summary = response.choices[0].message.content or ""
        logger.info("Summary generated successfully.")
        return summary.strip()
    except Exception as e:
        logger.error("OpenAI summarisation failed | error=%s", str(e))
        return "Error: Unable to generate summary at this time."


def ask_question(document_content: str, question: str) -> str:
    """Answer a contextual question about the given document content."""
    try:
        response = _get_client().chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that answers questions "
                        "based on the provided document content. Only answer "
                        "using information from the document."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Document:\n{document_content}\n\n"
                        f"Question: {question}"
                    ),
                },
            ],
            max_tokens=500,
            temperature=0.3,
        )
        answer = response.choices[0].message.content or ""
        logger.info("Question answered successfully.")
        return answer.strip()
    except Exception as e:
        logger.error("OpenAI question-answer failed | error=%s", str(e))
        return "Error: Unable to answer the question at this time."
