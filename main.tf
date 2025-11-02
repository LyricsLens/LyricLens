provider "aws" {
  region = var.aws_region
}

module "s3-website" {
  source      = "./modules/s3-website"
  bucket_name = var.bucket_name
  index_html  = var.index_html
}
module "dynamodb" {
  source        = "./modules/dynamodb"
  hash_key      = "id"
  attributes    = [{ name = "id", type = "S" }]
}
module "lambda" {
  source        = "./modules/lambdas"
  function_name = "lyric-lens-handler"
  filename      = "${path.module}/modules/lambdas/lambda_function.zip"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.11"
  environment = {
    TABLE_NAME = module.dynamodb.table_name
  }
}
module "api-gateway" {
  source      = "./modules/api-gateway"
  api_name    = "lyric-lens-rest-api"  
  images_path = "images"
  stage_name  = "dev"
  lambda_arn  = module.lambda.arn
}


terraform {
  required_version = ">= 1.11.0"
  backend "s3" {
    bucket         = "cumulonimbus-tf-state"
    key            = "swen514/prod/terraform.tfstate" # any path you like
    region         = "us-east-1"
    # dynamodb_table = "tf-locks"
    encrypt        = true
  }
}