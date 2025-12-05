variable "name" {
  type = string
}

variable "ami_id" {
  type = string
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "user_data" {
  type    = string
  default = ""
}

variable "target_group_arns" {
  type    = list(string)
  default = []
}

variable "min_size" {
  type    = number
  default = 1
}

variable "max_size" {
  type    = number
  default = 10
}

variable "desired_capacity" {
  type    = number
  default = 3
}

variable "instance_refresh_strategy" {
  type    = string
  default = "Rolling"
}

variable "instance_refresh_min_healthy_percentage" {
  type    = number
  default = 100
}

variable "instance_refresh_max_batch_size" {
  type    = number
  default = 1
}
