output "instance_ids" {
  description = "IDs des instances EC2"
  value       = aws_instance.sample_app[*].id
}

output "public_ips" {
  description = "IPs publiques des instances"
  value       = aws_instance.sample_app[*].public_ip
}

output "application_urls" {
  description = "URLs des applications"
  value       = [for ip in aws_instance.sample_app[*].public_ip : "http://${ip}:8080"]
}

output "security_group_id" {
  description = "ID du security group"
  value       = aws_security_group.sample_app.id
}
