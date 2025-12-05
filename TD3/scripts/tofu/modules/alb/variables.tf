variable "name" {
  description = "Name of the ALB"
  type        = string
}

variable "alb_http_port" {
  description = "ALB HTTP port"
  type        = number
  default     = 80
}

variable "app_http_port" {
  description = "Application HTTP port"
  type        = number
  default     = 8080
}

variable "app_health_check_path" {
  description = "Health check path"
  type        = string
  default     = "/"
}
