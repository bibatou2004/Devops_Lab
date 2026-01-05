variable "endpoint" {
  description = "The endpoint URL to test"
  type        = string
}

variable "expected_status" {
  description = "Expected HTTP status code"
  type        = number
  default     = 200
}

variable "expected_body" {
  description = "Expected response body (optional)"
  type        = string
  default     = ""
}
