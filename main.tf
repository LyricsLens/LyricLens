provider "aws" {
  region = var.aws_region
}

module "s3-website" {
  source      = "./modules/s3-website"
}
module "dynamodb" {
  source        = "./modules/dynamodb"
  hash_key      = "id"
  attributes    = [{ name = "id", type = "S" }]
}


terraform {
  required_version = ">= 1.11.0"
}