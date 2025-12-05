variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "lambda-sample"
}

variable "runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.11"
}

variable "timeout" {
  description = "Lambda timeout in seconds"
  type        = number
  default     = 30
}

variable "source_dir" {
  description = "Path to Lambda source code directory"
  type        = string
}

variable "environment_variables" {
  description = "Environment variables for Lambda"
  type        = map(string)
  default     = {}
}
