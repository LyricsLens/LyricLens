# REST API
resource "aws_api_gateway_rest_api" "api" {
  name        = var.api_name
  description = "Lyric Lens REST API"
}

# Resource: /images
resource "aws_api_gateway_resource" "images" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = var.images_path
}

# GET /images
resource "aws_api_gateway_method" "get_all" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.images.id
  http_method   = "GET"
  authorization = "NONE"
}

# Resource: /images/{id}
resource "aws_api_gateway_resource" "image_id" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_resource.images.id
  path_part   = "{id}"
}

# GET /images/{id}
resource "aws_api_gateway_method" "get_by_id" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.image_id.id
  http_method   = "GET"
  authorization = "NONE"
}

# POST /images
resource "aws_api_gateway_method" "post_image" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.images.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_all_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.images.id
  http_method             = aws_api_gateway_method.get_all.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = var.lambda_arn
}

resource "aws_api_gateway_integration" "get_by_id_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.image_id.id
  http_method             = aws_api_gateway_method.get_by_id.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = var.lambda_arn
}

resource "aws_api_gateway_integration" "post_image_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.images.id
  http_method             = aws_api_gateway_method.post_image.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = var.lambda_arn
}

# Deployment
resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [
    aws_api_gateway_method.get_all,
    aws_api_gateway_method.get_by_id,
    aws_api_gateway_method.post_image
  ]
  rest_api_id = aws_api_gateway_rest_api.api.id
}

# Stage
resource "aws_api_gateway_stage" "dev" {
  stage_name    = var.stage_name
  rest_api_id   = aws_api_gateway_rest_api.api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}
