# CloudWatch Log Group for governance audit trail (SR4, NFR6)

resource "aws_cloudwatch_log_group" "app_logs" {
  name              = "/ai-governance-assistant/application"
  retention_in_days = 90

  tags = {
    Project     = "AI-Governance-Assistant"
    Environment = var.environment
    Purpose     = "Governance-Audit-Trail"
  }
}

# CloudWatch Metric Alarm — High Error Rate
resource "aws_cloudwatch_metric_alarm" "high_error_rate" {
  alarm_name          = "ai-governance-high-error-rate"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "5XXError"
  namespace           = "AWS/ApiGateway"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  alarm_description   = "Triggers when 5xx errors exceed 10 in 5 minutes"

  tags = {
    Project = "AI-Governance-Assistant"
  }
}

# CloudWatch Metric Alarm — High Latency
resource "aws_cloudwatch_metric_alarm" "high_latency" {
  alarm_name          = "ai-governance-high-latency"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 3
  metric_name         = "Latency"
  namespace           = "AWS/ApiGateway"
  period              = 300
  statistic           = "Average"
  threshold           = 5000
  alarm_description   = "Triggers when average latency exceeds 5 seconds"

  tags = {
    Project = "AI-Governance-Assistant"
  }
}

# CloudWatch Dashboard
resource "aws_cloudwatch_dashboard" "main" {
  dashboard_name = "AI-Governance-Assistant"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          title   = "API Request Count"
          metrics = [["AWS/ApiGateway", "Count", "ApiName", "AI-Governance-API"]]
          period  = 300
          stat    = "Sum"
          region  = var.aws_region
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        properties = {
          title   = "API Latency (ms)"
          metrics = [["AWS/ApiGateway", "Latency", "ApiName", "AI-Governance-API"]]
          period  = 300
          stat    = "Average"
          region  = var.aws_region
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 6
        width  = 12
        height = 6
        properties = {
          title   = "5XX Errors"
          metrics = [["AWS/ApiGateway", "5XXError", "ApiName", "AI-Governance-API"]]
          period  = 300
          stat    = "Sum"
          region  = var.aws_region
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 6
        width  = 12
        height = 6
        properties = {
          title   = "S3 Bucket Size (Bytes)"
          metrics = [["AWS/S3", "BucketSizeBytes", "BucketName", var.s3_bucket_name, "StorageType", "StandardStorage"]]
          period  = 86400
          stat    = "Average"
          region  = var.aws_region
        }
      }
    ]
  })
}
