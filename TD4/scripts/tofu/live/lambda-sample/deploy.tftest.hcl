# Tests Terraform locaux

run "deploy" {
  command = apply
}

run "validate_infrastructure" {
  command = plan

  assert {
    condition     = output.lambda_function_arn != ""
    error_message = "Lambda ARN output is empty"
  }

  assert {
    condition     = output.api_endpoint == "http://localhost:8080"
    error_message = "API endpoint does not match expected value"
  }

  assert {
    condition     = output.deployment_file != ""
    error_message = "Deployment file output is empty"
  }
}
