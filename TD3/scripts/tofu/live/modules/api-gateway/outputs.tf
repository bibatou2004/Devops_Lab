output "api_endpoint" {
  description = "API Gateway endpoint"
  value       = "${aws_apigatewayv2_api.this.api_endpoint}/"
}

output "api_id" {
  description = "API Gateway API ID"
  value       = aws_apigatewayv2_api.this.id
}
