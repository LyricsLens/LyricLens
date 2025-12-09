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
  image_bucket_arn = module.s3-website.bucket_arn
  environment = {
    IMAGE_BUCKET           =  module.s3-website.bucket_name  # <----- WHERE IMAGES ARE STORED
		BEDROCK_IMAGE_MODEL_ID = var.bedrock_image_model_id,
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
  themes_path = "themes"
  stage_name  = "dev"
  lambda_arn  = module.lambda.arn
  aws_region = var.aws_region

  songs_path = "songs"
  allowed_origins  = [
    "http://localhost:3000",
    "http://${module.s3-website.website_endpoint}",
  ]
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