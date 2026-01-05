variable "aws_region" {
  description = "Région AWS"
  type        = string
  default     = "us-east-2"
}

variable "provider_url" {
  description = "URL du fournisseur OIDC GitHub"
  type        = string
  default     = "https://token.actions.githubusercontent.com"
}

variable "audience" {
  description = "Audience OIDC"
  type        = string
  default     = "sts.amazonaws.com"
}
