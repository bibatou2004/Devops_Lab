output "status_code" {
  description = "HTTP status code of the endpoint"
  value       = data.http.test_endpoint.status_code
}

output "response_body" {
  description = "Response body from the endpoint"
  value       = data.http.test_endpoint.response_body
}

output "headers" {
  description = "Response headers"
  value       = data.http.test_endpoint.response_headers
}
