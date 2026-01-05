variable "name" {
  description = "Name of S3 bucket for Terraform state"
  type        = string
}

variable "dynamodb_table" {
  description = "Name of DynamoDB table for state locking"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "enable_versioning" {
  description = "Enable S3 versioning"
  type        = bool
  default     = true
}
