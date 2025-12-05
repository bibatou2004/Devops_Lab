variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "state_bucket_name" {
  description = "Name of S3 bucket for Terraform state"
  type        = string
  default     = "bibawandaogo-devops-tfstate"
}

variable "dynamodb_table_name" {
  description = "Name of DynamoDB table for state locking"
  type        = string
  default     = "bibawandaogo-devops-tfstate-lock"
}
