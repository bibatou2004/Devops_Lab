output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.app.dns_name
}

output "alb_arn" {
  description = "ARN of the load balancer"
  value       = aws_lb.app.arn
}

output "asg_name" {
  description = "Name of the Auto Scaling Group"
  value       = aws_autoscaling_group.app.name
}

output "alb_name" {
  description = "Name of the load balancer"
  value       = aws_lb.app.name
}
