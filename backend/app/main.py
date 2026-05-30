"""
Cloud-Based AI Governance & Knowledge Assistant
Main FastAPI application entry point.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import upload, summarise, ask, health
from app.utils.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Governance & Knowledge Assistant",
    description="Cloud-based AI assistant with governance, auditing, and secure architecture.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["Health"])
app.include_router(upload.router, tags=["Upload"])
app.include_router(summarise.router, tags=["Summarise"])
app.include_router(ask.router, tags=["Ask"])

logger.info("AI Governance & Knowledge Assistant started.")
