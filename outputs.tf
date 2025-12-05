output "oidc_provider_arn" {
  description = "ARN du fournisseur OIDC GitHub"
  value       = module.oidc_provider.oidc_provider_arn
}

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
