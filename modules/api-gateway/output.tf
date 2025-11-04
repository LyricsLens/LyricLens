# api-gateway/output.tf
output "api_invoke_url" {
  description = "The base URL to invoke the API Gateway"
  value       = "${aws_api_gateway_stage.dev.invoke_url}"
}