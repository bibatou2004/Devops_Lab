output "s3_bucket_name" {
  description = "Name of S3 bucket for state"
  value       = module.state.s3_bucket_name
}

output "dynamodb_table_name" {
  description = "Name of DynamoDB table for locking"
  value       = module.state.dynamodb_table_name
}
