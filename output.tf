output "website_url" {
  description = "Public S3 Website URL"
  value       = "http://${aws_s3_bucket_website_configuration.site.website_endpoint}"
}

output "bucket_name" {
  description = "Created bucket name"
  value       = aws_s3_bucket.site.bucket
}