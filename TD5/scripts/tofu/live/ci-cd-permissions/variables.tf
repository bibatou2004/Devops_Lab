variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "github_repo" {
  description = "GitHub repository (owner/repo)"
  type        = string
  default     = "bibatou2004/Devops_Lab"
}

variable "name" {
  description = "Base name for resources"
  type        = string
  default     = "lambda-sample"
}

variable "lambda_env_vars" {
  description = "Environment variables for Lambda"
  type        = map(string)
  default = {
    ENVIRONMENT = "production"
    VERSION     = "1.0.0"
  }
}
