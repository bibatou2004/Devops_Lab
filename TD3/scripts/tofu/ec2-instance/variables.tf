variable "ami_id" {
  description = "The ID of the AMI to run"
  type        = string
}

variable "instance_type" {
  description = "The instance type"
  type        = string
  default     = "t3.micro"
}

variable "instance_count" {
  description = "Number of instances to create"
  type        = number
  default     = 1
}
