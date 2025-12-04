output "instance_ids" {
  description = "IDs of the EC2 instances"
  value       = aws_instance.sample_app[*].id
}

output "public_ips" {
  description = "Public IPs of the EC2 instances"
  value       = aws_instance.sample_app[*].public_ip
}

output "application_urls" {
  description = "URLs to access the applications"
  value       = [for ip in aws_instance.sample_app[*].public_ip : "http://${ip}:8080"]
}

output "security_group_id" {
  description = "The ID of the security group"
  value       = aws_security_group.sample_app.id
}
