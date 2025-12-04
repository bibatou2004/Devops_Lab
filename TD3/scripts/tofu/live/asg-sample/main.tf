terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Data source for default VPC
data "aws_vpc" "default" {
  default = true
}

# Data source for default subnets
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Launch Template
resource "aws_launch_template" "app" {
  name_prefix   = "sample-app-"
  image_id      = var.ami_id
  instance_type = "t3.micro"

  user_data = base64encode(<<-EOF
              #!/bin/bash
              cd /home/app-user
              pm2 start app.js --name "sample-app"
              pm2 save
              EOF
  )

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name = "sample-app-instance"
    }
  }
}

# Security Group for ALB
resource "aws_security_group" "alb" {
  name        = "sample-app-alb-sg"
  description = "Security group for ALB"
  vpc_id      = data.aws_vpc.default.id
  revoke_rules_on_delete = true

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "sample-app-alb-sg"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Security Group for Instances
resource "aws_security_group" "app" {
  name        = "sample-app-sg-new-v2"
  description = "Security group for app instances"
  vpc_id      = data.aws_vpc.default.id
  revoke_rules_on_delete = true

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "sample-app-sg-new"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Application Load Balancer
resource "aws_lb" "app" {
  name               = "sample-app-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = data.aws_subnets.default.ids

  tags = {
    Name = "sample-app-alb"
  }
}

# Target Group
resource "aws_lb_target_group" "app" {
  name        = "sample-app-tg"
  port        = 8080
  protocol    = "HTTP"
  vpc_id      = data.aws_vpc.default.id
  target_type = "instance"

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    interval            = 30
    path                = "/"
    matcher             = "200"
  }

  tags = {
    Name = "sample-app-tg"
  }
}

# ALB Listener
resource "aws_lb_listener" "app" {
  load_balancer_arn = aws_lb.app.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "app" {
  name                = "sample-app-asg"
  vpc_zone_identifier = data.aws_subnets.default.ids
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300

  min_size         = 3
  max_size         = 6
  desired_capacity = 3

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "sample-app-instance"
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
}
