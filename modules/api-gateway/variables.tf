variable "api_name" {
  type        = string
  description = "Name of the API Gateway REST API"
  default     = "lyric-lens-rest-api"
}

variable "images_path" {
  type        = string
  description = "Path for the images resource"
  default     = "images"
}

variable "stage_name" {
  type        = string
  description = "Stage name for the API deployment"
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region to deploy the API Gateway"
  type        = string
}

variable "lambda_arn" {
  description = "ARN of the Lambda function to integrate with API Gateway"
  type        = string
}
