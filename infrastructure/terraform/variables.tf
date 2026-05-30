variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "eu-west-1"
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket for document storage"
  type        = string
  default     = "ai-governance-docs"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
