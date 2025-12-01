variable "bedrock_image_model_id" {
	type    = string
	default = "amazon.titan-image-generator-v2:0"
}
variable "aws_region" {
  type        = string
  default     = "us-east-1"
}
variable "bucket_name" {
  type        = string
  default     = "lyriclens.cumulocrew"
}
variable "index_html" {
  type        = string
  default     = "<h1>Welcome to LyricLens!</h1>"
}

variable "bucket_base" {
  type        = string
  description = "base name for s3 bucket"
  default     = "lyriclens"
}