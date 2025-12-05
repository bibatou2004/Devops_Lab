# OIDC Outputs
output "oidc_provider_arn" {
  description = "ARN du fournisseur OIDC"
  value       = module.oidc_provider.oidc_provider_arn
}

# IAM Roles Outputs
output "lambda_test_role_arn" {
  description = "ARN du rôle IAM pour les tests"
  value       = module.iam_roles.lambda_test_role_arn
}

output "lambda_deploy_plan_role_arn" {
  description = "ARN du rôle IAM pour le plan"
  value       = module.iam_roles.lambda_deploy_plan_role_arn
}

output "lambda_deploy_apply_role_arn" {
  description = "ARN du rôle IAM pour l'apply"
  value       = module.iam_roles.lambda_deploy_apply_role_arn
}

# Lambda Outputs
output "lambda_function_arn" {
  description = "ARN de la fonction Lambda"
  value       = module.lambda_function.function_arn
}

output "lambda_function_name" {
  description = "Nom de la fonction Lambda"
  value       = module.lambda_function.function_name
}

# API Gateway Outputs
output "api_endpoint" {
  description = "URL de l'API Gateway"
  value       = module.api_gateway.api_endpoint
  
  # Affichez l'URL complète pour les tests
  sensitive = false
}

output "api_id" {
  description = "ID de l'API Gateway"
  value       = module.api_gateway.api_id
}
