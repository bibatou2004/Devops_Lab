# Configuration Terraform Locale - DevOps Lab
# Cette configuration ne nécessite pas d'accès AWS

terraform {
  required_version = ">= 1.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

# === VARIABLES ===

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "test"
}

# === RESOURCES ===

# Créer un répertoire pour les résultats de test
resource "local_file" "lambda_config" {
  content = jsonencode({
    function_name = "devops-lab-test-function"
    runtime       = "nodejs18.x"
    handler       = "index.handler"
    role          = "arn:aws:iam::123456789012:role/lambda-test-role"
    memory_size   = 128
    timeout       = 30
  })
  filename = "${path.module}/lambda_config.json"
}

# Créer un fichier de résultat de déploiement
resource "local_file" "deployment_result" {
  content = templatefile("${path.module}/deployment_template.tpl", {
    function_name = "devops-lab-test-function"
    api_endpoint  = "http://localhost:8080"
    timestamp     = timestamp()
    status        = "deployed"
  })
  filename = "${path.module}/deployment_result.txt"
}

# Créer un fichier de configuration API
resource "local_file" "api_config" {
  content = jsonencode({
    api_name = "devops-lab-test-api"
    protocol = "HTTP"
    endpoint = "http://localhost:8080"
    routes = [
      {
        path    = "/"
        method  = "GET"
        handler = "index.handler"
      },
      {
        path    = "/name/{name}"
        method  = "GET"
        handler = "index.handler"
      },
      {
        path    = "/add/{a}/{b}"
        method  = "GET"
        handler = "index.handler"
      }
    ]
  })
  filename = "${path.module}/api_config.json"
}

# === OUTPUTS ===

output "lambda_function_arn" {
  description = "Lambda function ARN (mock)"
  value       = "arn:aws:lambda:us-east-1:123456789012:function:devops-lab-test-function"
}

output "api_endpoint" {
  description = "API Gateway endpoint"
  value       = "http://localhost:8080"
}

output "deployment_file" {
  description = "Path to deployment result file"
  value       = local_file.deployment_result.filename
}

output "lambda_config_file" {
  description = "Path to Lambda configuration file"
  value       = local_file.lambda_config.filename
}

output "api_config_file" {
  description = "Path to API configuration file"
  value       = local_file.api_config.filename
}
