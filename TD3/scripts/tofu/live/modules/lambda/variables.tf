variable "name" {
  description = "Lambda function name"
  type        = string
}

variable "src_dir" {
  description = "Source directory for Lambda function"
  type        = string
}

variable "runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "nodejs20.x"
}

variable "handler" {
  description = "Lambda handler"
  type        = string
}

variable "memory_size" {
  description = "Lambda memory size"
  type        = number
  default     = 128
}

variable "timeout" {
  description = "Lambda timeout"
  type        = number
  default     = 5
}

variable "environment_variables" {
  description = "Environment variables"
  type        = map(string)
  default     = {}
}
