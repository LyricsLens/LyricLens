provider "aws" {
  region = var.aws_region
}

module "s3-website" {
  source      = "./modules/s3-website"
}

terraform {
  required_version = ">= 1.11.0"
}