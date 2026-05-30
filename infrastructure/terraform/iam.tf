# IAM Role for EC2 instance — Least Privilege (SR3)

resource "aws_iam_role" "app_role" {
  name = "ai-governance-app-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Project = "AI-Governance-Assistant"
  }
}

# S3 access policy — scoped to specific bucket only
resource "aws_iam_role_policy" "s3_access" {
  name = "s3-document-access"
  role = aws_iam_role.app_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.documents.arn,
          "${aws_s3_bucket.documents.arn}/*"
        ]
      }
    ]
  })
}

# CloudWatch Logs policy — write logs only
resource "aws_iam_role_policy" "cloudwatch_logs" {
  name = "cloudwatch-logs-write"
  role = aws_iam_role.app_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:${var.aws_region}:*:*"
      }
    ]
  })
}

# Instance profile to attach role to EC2
resource "aws_iam_instance_profile" "app_profile" {
  name = "ai-governance-app-profile"
  role = aws_iam_role.app_role.name
}
