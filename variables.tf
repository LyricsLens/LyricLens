variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "S3 bucket name"
  type        = string
  default     = "lyriclens.cumulocrew"
}

variable "index_html" {
  description = "Inline HTML for index page (ignored if index_path is set)"
  type        = string
  default     = "<h1>Welcome to LyricLens!</h1>"
}
