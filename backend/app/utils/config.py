"""Application configuration loaded from environment variables."""

import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Application settings sourced from environment variables."""

    aws_region: str = os.getenv("AWS_REGION", "eu-west-1")
    s3_bucket_name: str = os.getenv("S3_BUCKET_NAME", "ai-governance-docs")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
