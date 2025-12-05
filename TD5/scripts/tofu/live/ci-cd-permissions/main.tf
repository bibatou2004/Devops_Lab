module "oidc_provider" {
  source = "../../modules/github-aws-oidc"
  
  aws_region = var.aws_region
}

module "iam_roles" {
  source = "../../modules/gh-actions-iam-roles"

  oidc_provider_arn = module.oidc_provider.oidc_provider_arn
  github_repo       = var.github_repo
  name              = var.name
}
