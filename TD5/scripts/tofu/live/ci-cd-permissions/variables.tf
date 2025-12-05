variable "aws_region" {
  description = "Région AWS"
  type        = string
  default     = "us-east-2"
}

variable "github_repo" {
  description = "Dépôt GitHub (owner/repo)"
  type        = string
  default     = "bibatou2004/Devops_Lab"
}

variable "name" {
  description = "Nom de base pour les ressources"
  type        = string
  default     = "lambda-sample"
}
