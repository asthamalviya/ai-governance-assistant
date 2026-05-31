"""S3 storage service for document management."""

import logging
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from app.utils.config import settings

logger = logging.getLogger(__name__)

_s3_client = None


def _get_s3_client():
    """Lazy-initialise the S3 client."""
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client("s3", region_name=settings.aws_region)
    return _s3_client


def upload_to_s3(content: bytes, s3_key: str, content_type: str) -> None:
    """Upload file content to S3."""
    try:
        _get_s3_client().put_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key,
            Body=content,
            ContentType=content_type,
            ServerSideEncryption="AES256",
        )
        logger.info("Uploaded to S3 | key=%s", s3_key)
    except ClientError as e:
        logger.error("S3 upload failed | key=%s | error=%s", s3_key, str(e))
        raise


def get_document_content(s3_key: str) -> Optional[str]:
    """Retrieve document text content from S3."""
    try:
        response = _get_s3_client().get_object(
            Bucket=settings.s3_bucket_name,
            Key=s3_key,
        )
        body = response["Body"].read().decode("utf-8")
        logger.info("Retrieved from S3 | key=%s", s3_key)
        return body
    except ClientError as e:
        logger.error("S3 retrieval failed | key=%s | error=%s", s3_key, str(e))
        return None
