variable "aws_region" {
  description = "Région AWS"
  type        = string
  default     = "us-east-2"
}

variable "github_repo" {
  description = "Dépôt GitHub (format: owner/repo)"
  type        = string
  default     = "bibatou2004/Devops_Lab"
}

variable "name" {
  description = "Nom de base pour les rôles IAM"
  type        = string
  default     = "lambda-sample"
}

variable "enable_iam_role_for_testing" {
  description = "Créer le rôle IAM pour les tests"
  type        = bool
  default     = true
}

variable "enable_iam_role_for_plan" {
  description = "Créer le rôle IAM pour le plan"
  type        = bool
  default     = true
}

variable "enable_iam_role_for_apply" {
  description = "Créer le rôle IAM pour l'apply"
  type        = bool
  default     = true
}
