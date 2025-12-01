variable "function_name" {}
variable "filename" {}
variable "handler" {}
variable "runtime" {}

variable "environment" {
  type = map(string)
  default = {}
}
variable "dynamodb_table_arn" {
  type        = string
}

variable "image_bucket_arn" {
  type        = string
}