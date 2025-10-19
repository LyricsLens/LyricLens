# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"  # Set AWS region to US East 1 (N. Virginia)
}

# Local variables block for configuration values
locals {
    aws_key = "SWEN_AWS_KEY"   # SSH key pair name for EC2 instance access
}

terraform {
  required_version = ">= 1.11.0"
  backend "s3" {
    bucket = "github-devops-bucket9468"
    key = "prod/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
    use_lockfile = true
  }
}