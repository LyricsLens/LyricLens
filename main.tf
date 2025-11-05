provider "aws" {
  region = var.aws_region
}

module "s3-website" {
  source      = "./modules/s3-website"
  bucket_base = var.bucket_base
  index_html  = var.index_html
}
resource "aws_s3_account_public_access_block" "this" {
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
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
    TABLE_NAME = module.dynamodb.table_name,
    ALLOWED_ORIGINS = join(",", [
      "http://localhost:3000",
      "http://${module.s3-website.website_endpoint}",
    ])
  }
  dynamodb_table_arn = module.dynamodb.table_arn
}
module "api-gateway" {
  source      = "./modules/api-gateway"
  api_name    = "lyric-lens-rest-api"  
  images_path = "images"
  stage_name  = "dev"
  lambda_arn  = module.lambda.arn
  aws_region = var.aws_region

  songs_path = "songs"
  allowed_origins  = [
    "http://localhost:3000",
    "http://${module.s3-website.website_endpoint}",
  ]
}

module "bedrock_lambda" {
  source        = "./modules/bedrock-lambda"

  function_name = "bedrock-image-generator"
  filename      = "${path.module}/modules/lambda-bedrock/bedrock_lambda.zip"
  handler       = "bedrock_lambda.handler"
  runtime       = "python3.11"

  bucket_name   = module.s3-website.bucket_name
  bucket_arn    = module.s3-website.bucket_arn
  image_prefix  = "generated/"

  model_id      = var.bedrock_model_id   # define in variables.tf or tfvars
  aws_region    = var.aws_region
  url_expiry_secs = 900

  timeout      = 60
  memory_size  = 1024

  tags = {
    Project = "lyric-lens"
  }
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