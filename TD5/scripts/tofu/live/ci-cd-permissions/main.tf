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

module "lambda_function" {
  source = "../../modules/lambda-function"

  function_name         = var.name
  runtime               = "python3.11"
  timeout               = 30
  source_dir            = "${path.module}/../../../sample-app/src"
  environment_variables = var.lambda_env_vars
}

module "api_gateway" {
  source = "../../modules/api-gateway"

  api_name              = "${var.name}-api"
  aws_region            = var.aws_region
  lambda_function_arn   = module.lambda_function.function_arn
  lambda_function_name  = module.lambda_function.function_name
}
