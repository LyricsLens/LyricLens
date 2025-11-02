variable "function_name" {}
variable "filename" {}
variable "handler" {}
variable "runtime" {}
variable "environment" {
  type = map(string)
  default = {}
}
