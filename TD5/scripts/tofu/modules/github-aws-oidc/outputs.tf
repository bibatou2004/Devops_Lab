output "oidc_provider_arn" {
  description = "ARN du fournisseur OIDC GitHub"
  value       = aws_iam_openid_connect_provider.github.arn
}

output "oidc_provider_url" {
  description = "URL du fournisseur OIDC"
  value       = aws_iam_openid_connect_provider.github.url
}
