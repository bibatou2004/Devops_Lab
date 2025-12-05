provider "aws" {
  region = var.aws_region
}

# Module OIDC Provider
module "oidc_provider" {
  source = "../../modules/github-aws-oidc"

  aws_region = var.aws_region
}

# Module IAM Roles
module "iam_roles" {
  source = "../../modules/gh-actions-iam-roles"

  aws_region        = var.aws_region
  oidc_provider_arn = module.oidc_provider.oidc_provider_arn
  github_repo       = var.github_repo
  
  name                            = var.name
  enable_iam_role_for_testing     = var.enable_iam_role_for_testing
  enable_iam_role_for_plan        = var.enable_iam_role_for_plan
  enable_iam_role_for_apply       = var.enable_iam_role_for_apply
}
