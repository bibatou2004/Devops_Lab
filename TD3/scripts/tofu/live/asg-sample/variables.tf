variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "ami_id" {
  description = "AMI ID for the instances"
  type        = string
}
