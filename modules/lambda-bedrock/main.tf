locals {
  env = {
    BUCKET_NAME     = var.bucket_name
    IMAGE_PREFIX    = var.image_prefix
    MODEL_ID        = var.model_id
    URL_EXPIRY_SECS = tostring(var.url_expiry_secs)
    AWS_REGION      = var.aws_region
  }
}

# --- IAM role for Lambda ---
data "aws_iam_policy_document" "assume_lambda" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "this" {
  name               = "${var.function_name}-role"
  assume_role_policy = data.aws_iam_policy_document.assume_lambda.json
  tags               = var.tags
}

resource "aws_iam_role_policy_attachment" "logs" {
  role       = aws_iam_role.this.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# S3 write + read for the website bucket (prefix + list)
data "aws_iam_policy_document" "s3_write" {
  statement {
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = [var.bucket_arn]
  }
  statement {
    effect    = "Allow"
    actions   = ["s3:PutObject", "s3:GetObject", "s3:AbortMultipartUpload"]
    resources = ["${var.bucket_arn}/*"]
  }
}

resource "aws_iam_policy" "s3_write" {
  name   = "${var.function_name}-s3"
  policy = data.aws_iam_policy_document.s3_write.json
}

resource "aws_iam_role_policy_attachment" "s3_write" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.s3_write.arn
}

# Bedrock invoke
data "aws_iam_policy_document" "bedrock" {
  statement {
    effect    = "Allow"
    actions   = ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"]
    resources = ["*"] # tighten to specific model ARN if desired
  }
}

resource "aws_iam_policy" "bedrock" {
  name   = "${var.function_name}-bedrock"
  policy = data.aws_iam_policy_document.bedrock.json
}

resource "aws_iam_role_policy_attachment" "bedrock" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.bedrock.arn
}

# --- Lambda function ---
resource "aws_lambda_function" "this" {
  function_name = var.function_name
  role          = aws_iam_role.this.arn
  handler       = var.handler
  runtime       = var.runtime
  filename      = var.filename

  timeout     = var.timeout
  memory_size = var.memory_size

  environment { variables = local.env }

  tags = var.tags
}
