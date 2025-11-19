# api-gateway/main.tf
# =========================
# REST API
# =========================
resource "aws_api_gateway_rest_api" "api" {
  name        = var.api_name
  description = "Lyric Lens REST API"
}

# ---------- Resources ----------
resource "aws_api_gateway_resource" "images" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = var.images_path
}

resource "aws_api_gateway_resource" "image_id" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_resource.images.id
  path_part   = "{id}"
}

resource "aws_api_gateway_resource" "songs" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = var.songs_path
}

# ---------- Methods (GET/POST) ----------
resource "aws_api_gateway_method" "get_all" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.images.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "get_by_id" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.image_id.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "post_image" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.images.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "get_songs_with_lyrics" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.songs.id
  http_method   = "GET"
  authorization = "NONE"
}

# ---------- MOCK OPTIONS (CORS preflight) ----------
# /images
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
    "method.response.header.Access-Control-Allow-Origin"      = "'*'"
    "method.response.header.Access-Control-Allow-Headers"     = "'Content-Type,Authorization'"
    "method.response.header.Access-Control-Allow-Methods"     = "'GET,POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Credentials" = "'false'"
    "method.response.header.Vary"                             = "'Origin'"
  }
  depends_on = [
    aws_api_gateway_integration.images_options
  ]
}

# /images/{id}
resource "aws_api_gateway_method" "image_id_options" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.image_id.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "image_id_options" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.image_id.id
  http_method = aws_api_gateway_method.image_id_options.http_method
  type        = "MOCK"
  request_templates = {
    "application/json" = "{\"statusCode\": 200}"
  }
}

resource "aws_api_gateway_method_response" "image_id_options_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.image_id.id
  http_method = aws_api_gateway_method.image_id_options.http_method
  status_code = "200"
  
  response_models = {
    "application/json" = "Empty"
  }
  
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"      = true
    "method.response.header.Access-Control-Allow-Headers"     = true
    "method.response.header.Access-Control-Allow-Methods"     = true
    "method.response.header.Access-Control-Allow-Credentials" = true
    "method.response.header.Vary"                             = true
  }
}

resource "aws_api_gateway_integration_response" "image_id_options_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.image_id.id
  http_method = aws_api_gateway_method.image_id_options.http_method
  status_code = aws_api_gateway_method_response.image_id_options_200.status_code
  
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"      = "'*'"
    "method.response.header.Access-Control-Allow-Headers"     = "'Content-Type,Authorization'"
    "method.response.header.Access-Control-Allow-Methods"     = "'GET,OPTIONS'"
    "method.response.header.Access-Control-Allow-Credentials" = "'false'"
    "method.response.header.Vary"                             = "'Origin'"
  }
  
  depends_on = [
    aws_api_gateway_integration.image_id_options
  ]
}

# /songs
resource "aws_api_gateway_method" "songs_options" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.songs.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "songs_options" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.songs.id
  http_method = aws_api_gateway_method.songs_options.http_method
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

# IMPORTANT: use ONE origin or '*' (not a comma list). If '*', credentials must be false.
resource "aws_api_gateway_integration_response" "songs_options_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.songs.id
  http_method = aws_api_gateway_method.songs_options.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"      = "'*'"
    "method.response.header.Access-Control-Allow-Headers"     = "'Content-Type,Authorization'"
    "method.response.header.Access-Control-Allow-Methods"     = "'GET,POST,OPTIONS'"
    "method.response.header.Access-Control-Allow-Credentials" = "'false'"
    "method.response.header.Vary"                             = "'Origin'"
  }
  depends_on = [ 
    aws_api_gateway_integration.songs_options
   ]
}

# ---------- Lambda proxy integrations ----------
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

# ---------- CORS for API Gateway-generated errors ----------
locals {
  cors_origin      = "'${join(",", var.allowed_origins)}'"
  cors_allow_hdrs  = "'Content-Type,Authorization'"
  cors_allow_meths = "'GET,POST,OPTIONS'"
}

resource "aws_api_gateway_gateway_response" "default_4xx" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  response_type = "DEFAULT_4XX"
  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin"      = "'*'"
    "gatewayresponse.header.Access-Control-Allow-Headers"     = "'Content-Type,Authorization'"
    "gatewayresponse.header.Access-Control-Allow-Methods"     = "'GET,POST,OPTIONS'"
    "gatewayresponse.header.Access-Control-Allow-Credentials" = "'false'"
    "gatewayresponse.header.Vary"                             = "'Origin'"
  }
}

resource "aws_api_gateway_gateway_response" "default_5xx" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  response_type = "DEFAULT_5XX"
  response_parameters = {
    "gatewayresponse.header.Access-Control-Allow-Origin"      = "'*'"
    "gatewayresponse.header.Access-Control-Allow-Headers"     = "'Content-Type,Authorization'"
    "gatewayresponse.header.Access-Control-Allow-Methods"     = "'GET,POST,OPTIONS'"
    "gatewayresponse.header.Access-Control-Allow-Credentials" = "'false'"
    "gatewayresponse.header.Vary"                             = "'Origin'"
  }
}

# ---------- Permissions ----------
resource "aws_lambda_permission" "api_gw_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}

# ---------- Deployment & Stage ----------
resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.images.id,
      aws_api_gateway_resource.image_id.id,
      aws_api_gateway_resource.songs.id,
      aws_api_gateway_method.get_all.id,
      aws_api_gateway_method.get_by_id.id,
      aws_api_gateway_method.post_image.id,
      aws_api_gateway_method.get_songs_with_lyrics.id,
      aws_api_gateway_method.images_options.id,
      aws_api_gateway_method.image_id_options.id,
      aws_api_gateway_method.songs_options.id,
      aws_api_gateway_integration.get_all_integration.id,
      aws_api_gateway_integration.get_by_id_integration.id,
      aws_api_gateway_integration.post_image_integration.id,
      aws_api_gateway_integration.get_lyrics_integration.id,
      aws_api_gateway_integration.images_options.id,
      aws_api_gateway_integration.image_id_options.id,
      aws_api_gateway_integration.songs_options.id,
      aws_api_gateway_resource.themes.id,
      aws_api_gateway_method.get_themes.id,
      aws_api_gateway_method.themes_options.id,
      aws_api_gateway_integration.get_themes_integration.id,
      aws_api_gateway_integration.themes_options.id,
    ]))
  }
  
  lifecycle {
    create_before_destroy = true
  }
  
  depends_on = [
    aws_api_gateway_method.get_all,
    aws_api_gateway_method.get_by_id,
    aws_api_gateway_method.post_image,
    aws_api_gateway_method.get_songs_with_lyrics,
    aws_api_gateway_method.images_options,
    aws_api_gateway_method.image_id_options,
    aws_api_gateway_method.songs_options,
    aws_api_gateway_integration.get_all_integration,
    aws_api_gateway_integration.get_by_id_integration,
    aws_api_gateway_integration.post_image_integration,
    aws_api_gateway_integration.get_lyrics_integration,
    aws_api_gateway_integration.images_options,
    aws_api_gateway_integration.image_id_options,
    aws_api_gateway_integration.songs_options,
    aws_api_gateway_integration_response.images_options_200,
    aws_api_gateway_integration_response.image_id_options_200,
    aws_api_gateway_integration_response.songs_options_200,
    aws_api_gateway_method.get_themes,
    aws_api_gateway_method.themes_options,
    aws_api_gateway_integration.get_themes_integration,
    aws_api_gateway_integration.themes_options,
    aws_api_gateway_integration_response.themes_options_200,
  ]
}

resource "aws_api_gateway_stage" "dev" {
  stage_name    = var.stage_name
  rest_api_id   = aws_api_gateway_rest_api.api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}

# ---------- /themes Resource ----------
resource "aws_api_gateway_resource" "themes" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "themes"
}

# GET /themes method
resource "aws_api_gateway_method" "get_themes" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.themes.id
  http_method   = "GET"
  authorization = "NONE"
}

# Lambda integration for GET /themes
resource "aws_api_gateway_integration" "get_themes_integration" {
  rest_api_id             = aws_api_gateway_rest_api.api.id
  resource_id             = aws_api_gateway_resource.themes.id
  http_method             = aws_api_gateway_method.get_themes.http_method
  type                    = "AWS_PROXY"
  integration_http_method = "POST"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${var.lambda_arn}/invocations"
}

# OPTIONS /themes (CORS)
resource "aws_api_gateway_method" "themes_options" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.themes.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "themes_options" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.themes.id
  http_method = aws_api_gateway_method.themes_options.http_method
  type        = "MOCK"
  request_templates = { "application/json" = "{\"statusCode\": 200}" }
}

resource "aws_api_gateway_method_response" "themes_options_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.themes.id
  http_method = aws_api_gateway_method.themes_options.http_method
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

resource "aws_api_gateway_integration_response" "themes_options_200" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.themes.id
  http_method = aws_api_gateway_method.themes_options.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin"      = "'*'"
    "method.response.header.Access-Control-Allow-Headers"     = "'Content-Type,Authorization'"
    "method.response.header.Access-Control-Allow-Methods"     = "'GET,OPTIONS'"
    "method.response.header.Access-Control-Allow-Credentials" = "'false'"
    "method.response.header.Vary"                             = "'Origin'"
  }
  depends_on = [
    aws_api_gateway_integration.themes_options
  ]
}