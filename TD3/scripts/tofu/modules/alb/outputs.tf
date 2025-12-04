output "alb_arn" {
  description = "ALB ARN"
  value       = aws_lb.app.arn
}

output "alb_dns_name" {
  description = "ALB DNS name"
  value       = aws_lb.app.dns_name
}

output "alb_name" {
  description = "ALB name"
  value       = aws_lb.app.name
}

output "target_group_arn" {
  description = "Target group ARN"
  value       = aws_lb_target_group.app.arn
}

output "app_security_group_id" {
  description = "App security group ID"
  value       = aws_security_group.app.id
}
