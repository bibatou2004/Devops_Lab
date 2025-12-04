packer {
  required_plugins {
    amazon = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-2"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

source "amazon-ebs" "amazon_linux_2023" {
  ami_name      = "packer-sample-app-{{timestamp}}"
  instance_type = var.instance_type
  region        = var.aws_region

  source_ami_filter {
    filters = {
      name                = "al2023-ami-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    owners      = ["amazon"]
    most_recent = true
  }

  ssh_username = "ec2-user"
  
  tags = {
    Name        = "packer-sample-app"
    Environment = "dev"
    CreatedBy   = "Packer"
  }
}

build {
  sources = ["source.amazon-ebs.amazon_linux_2023"]

  provisioner "file" {
    sources     = ["app.js", "app.config.js"]
    destination = "/tmp/"
  }

  provisioner "shell" {
    inline = [
      "set -e",
      "echo '=== Updating system ==='",
      "sudo dnf update -y",
      
      "echo '=== Installing Node.js 18 LTS ==='",
      "sudo dnf install -y nodejs",
      
      "echo '=== Verifying Node.js installation ==='",
      "node --version",
      "npm --version",
      
      "echo '=== Creating app user ==='",
      "sudo useradd app-user || true",
      "sudo mkdir -p /home/app-user",
      "sudo mkdir -p /home/app-user/logs",
      
      "echo '=== Moving application files ==='",
      "sudo mv /tmp/app.js /tmp/app.config.js /home/app-user/",
      "sudo chown -R app-user:app-user /home/app-user",
      
      "echo '=== Installing PM2 globally ==='",
      "sudo npm install pm2@latest -g",
      "pm2 --version",
      
      "echo '=== Setting up PM2 startup script ==='",
      "sudo su - app-user -c 'pm2 startup systemd -u app-user --hp /home/app-user --no-daemon' || true",
      "sudo systemctl enable pm2-app-user || true",
      
      "echo '=== Build completed successfully! ==='"
    ]
  }

  post-processor "manifest" {
    output     = "manifest.json"
    strip_path = true
  }
}
