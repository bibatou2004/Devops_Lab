variable "ami_id" {
  description = "ID de l'AMI à utiliser"
  type        = string
}

variable "instance_type" {
  description = "Type d'instance EC2"
  type        = string
  default     = "t3.micro"
}

variable "instance_count" {
  description = "Nombre d'instances à créer"
  type        = number
  default     = 1
}

variable "name" {
  description = "Nom de l'application"
  type        = string
  default     = "sample-app"
}

variable "security_group_name" {
  description = "Nom du security group"
  type        = string
  default     = "sample-app-sg"
}

variable "environment" {
  description = "Environnement (dev, staging, prod)"
  type        = string
  default     = "dev"
}
