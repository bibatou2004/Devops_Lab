output "api_endpoint" {
  description = "The API Gateway endpoint"
  value       = module.gateway.api_endpoint
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = module.function.function_name
}
