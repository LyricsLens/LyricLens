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

# Resource : /songs
resource "aws_api_gateway_resource" "songs" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = var.songs_path
}

resource "aws_api_gateway_method" "song_options" {
  rest_api_id   = aws_api_gateway_rest_api.api.id 
  resource_id   = aws_api_gateway_resource.songs.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

# GET /songs
resource "aws_api_gateway_method" "get_songs_with_lyrics" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.songs.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_all_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.images.id
  http_method             = aws_api_gateway_method.get_all.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${var.lambda_arn}/invocations"
}

resource "aws_api_gateway_integration" "get_by_id_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.image_id.id
  http_method             = aws_api_gateway_method.get_by_id.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${var.lambda_arn}/invocations"
}

resource "aws_api_gateway_integration" "post_image_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.images.id
  http_method             = aws_api_gateway_method.post_image.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${var.lambda_arn}/invocations"
}

resource "aws_api_gateway_integration" "get_lyrics_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.songs.id
  http_method             = aws_api_gateway_method.get_songs_with_lyrics.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${var.lambda_arn}/invocations"
}

resource "aws_api_gateway_integration" "songs_options" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.songs.id
  http_method = aws_api_gateway_method.songs_options.http_method
  type        = "MOCK"
  request_templates = { "application/json" = "{\"statusCode\": 200}" }
}

resource "aws_api_gateway_method" "images_options" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.images.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "images_options" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.images.id
  http_method = aws_api_gateway_method.images_options.http_method
  type        = "MOCK"
  request_templates = { "application/json" = "{\"statusCode\": 200}" }
}


resource "aws_api_gateway_method_response" "songs_options_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.songs.id
  http_method = aws_api_gateway_method.songs_options.http_method
  status_code = "200"
  response_models = { "application/json" = "Empty" }
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"      = true
    "method.response.header.Access-Control-Allow-Headers"     = true
    "method.response.header.Access-Control-Allow-Methods"     = true
    "method.response.header.Access-Control-Allow-Credentials" = true
    "method.response.header.Vary"                             = true
  }
}

resource "aws_api_gateway_method_response" "images_options_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.images.id
  http_method = aws_api_gateway_method.images_options.http_method
  status_code = "200"
  response_models = { "application/json" = "Empty" }
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"      = true
    "method.response.header.Access-Control-Allow-Headers"     = true
    "method.response.header.Access-Control-Allow-Methods"     = true
    "method.response.header.Access-Control-Allow-Credentials" = true
    "method.response.header.Vary"                             = true
  }
}

resource "aws_api_gateway_integration_response" "images_options_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.images.id
  http_method = aws_api_gateway_method.images_options.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"      = local.cors_origin
    "method.response.header.Access-Control-Allow-Headers"     = local.cors_allow_hdrs
    "method.response.header.Access-Control-Allow-Methods"     = local.cors_allow_meths
    "method.response.header.Access-Control-Allow-Credentials" = "'true'"
    "method.response.header.Vary"                             = "'Origin'"
  }
}

resource "aws_lambda_permission" "api_gw_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}


resource "aws_iam_role" "api_gw_cloudwatch" {
  name = "APIGatewayCloudWatchLogsRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "apigateway.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "api_gw_logs_policy" {
  role       = aws_iam_role.api_gw_cloudwatch.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

resource "aws_api_gateway_account" "account" {
  cloudwatch_role_arn = aws_iam_role.api_gw_cloudwatch.arn
}
# Deployment
resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  triggers = { redeploy = timestamp() }
  depends_on = [
    aws_api_gateway_method.get_all,
    aws_api_gateway_method.get_by_id,
    aws_api_gateway_method.post_image,
    aws_api_gateway_method.get_songs_with_lyrics,
    aws_api_gateway_integration.get_all_integration,
    aws_api_gateway_integration.get_by_id_integration,
    aws_api_gateway_integration.post_image_integration,
    aws_api_gateway_integration.get_lyrics_integration,
    aws_api_gateway_integration.songs_options,
    aws_api_gateway_integration.images_options,
    aws_api_gateway_gateway_response.default_4xx,
    aws_api_gateway_gateway_response.default_5xx,
  ]
}

# Stage
resource "aws_api_gateway_stage" "dev" {
  stage_name    = var.stage_name
  rest_api_id   = aws_api_gateway_rest_api.api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}

# Allowed origins — pass var.allowed_origins from root
locals {
  cors_origin      = "'${join(",", var.allowed_origins)}'"
  cors_allow_hdrs  = "'Content-Type,Authorization'"
  cors_allow_meths = "'GET,POST,OPTIONS'"
}

# CORS on API Gateway-generated 4XX
resource "aws_api_gateway_gateway_response" "default_4xx" {
  rest_api_id    = aws_api_gateway_rest_api.api.id
  response_type  = "DEFAULT_4XX"
  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin"      = "'${local.cors_origin}'"
    "gatewayresponse.header.Access-Control-Allow-Headers"     = "'${local.cors_allow_hdrs}'"
    "gatewayresponse.header.Access-Control-Allow-Methods"     = "'${local.cors_allow_meths}'"
    "gatewayresponse.header.Access-Control-Allow-Credentials" = "'true'"
    "gatewayresponse.header.Vary"                             = "'Origin'"
  }
}

# CORS on API Gateway-generated 5XX
resource "aws_api_gateway_gateway_response" "default_5xx" {
  rest_api_id    = aws_api_gateway_rest_api.api.id
  response_type  = "DEFAULT_5XX"
  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin"      = "'${local.cors_origin}'"
    "gatewayresponse.header.Access-Control-Allow-Headers"     = "'${local.cors_allow_hdrs}'"
    "gatewayresponse.header.Access-Control-Allow-Methods"     = "'${local.cors_allow_meths}'"
    "gatewayresponse.header.Access-Control-Allow-Credentials" = "'true'"
    "gatewayresponse.header.Vary"                             = "'Origin'"
  }
}

resource "aws_api_gateway_integration_response" "songs_options_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.songs.id
  http_method = aws_api_gateway_method.songs_options.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"      = local.cors_origin
    "method.response.header.Access-Control-Allow-Headers"     = local.cors_allow_hdrs
    "method.response.header.Access-Control-Allow-Methods"     = local.cors_allow_meths
    "method.response.header.Access-Control-Allow-Credentials" = "'true'"
    "method.response.header.Vary"                             = "'Origin'"
  }
}