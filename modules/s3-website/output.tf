output "website_url" {
  value       = "http://${aws_s3_bucket_website_configuration.site.website_endpoint}"
  description = "Public S3 website URL"
}

output "bucket_name" { 
    value = aws_s3_bucket.site.bucket
    description = "Bucket name"
}

output "bucket_arn" { 
    value = aws_s3_bucket.site.arn
    description = "Bucket ARN"
}
output "website_endpoint" {
  value = aws_s3_bucket_website_configuration.site.website_endpoint
}