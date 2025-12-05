variable "oidc_provider_arn" {
  description = "ARN du fournisseur OIDC GitHub"
  type        = string
}

variable "github_repo" {
  description = "Dépôt GitHub (format: owner/repo)"
  type        = string
}

variable "name" {
  description = "Nom de base pour les rôles IAM"
  type        = string
  default     = "github-actions"
}
