output "lambda_test_role_arn" {
  description = "ARN du rôle IAM pour les tests"
  value       = aws_iam_role.github_test_role.arn
}

output "lambda_deploy_plan_role_arn" {
  description = "ARN du rôle IAM pour le plan"
  value       = aws_iam_role.github_plan_role.arn
}

output "lambda_deploy_apply_role_arn" {
  description = "ARN du rôle IAM pour l'apply"
  value       = aws_iam_role.github_apply_role.arn
}
