variable "function_name" {}
variable "filename" {}
variable "handler" {}
variable "runtime" {}
variable "environment" {
  type = map(string)
  default = {}
}
variable "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table this Lambda can access"
  type        = string
}