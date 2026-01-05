# TD3 - DevOps Infrastructure as Code

## 📋 Overview

Complete DevOps pipeline using **Packer** (for AMI) and **Terraform** (for infrastructure) to deploy a scalable Node.js application on AWS.

## 🏗️ Architecture

```
                    Internet (0.0.0.0/0)
                            |
                       HTTP Port 80
                            |
                    ┌───────────────────┐
                    │  ALB               │
                    │ sample-app-alb     │
                    └─────────┬──────────┘
                              |
                         HTTP 8080
                              |
                    ┌─────────────────────┐
                    │  Target Group       │
                    │  sample-app-tg      │
                    └──────────┬──────────┘
                    ┌──────────┼──────────┐
                    |          |          |
              ┌─────▼──┐ ┌────▼──┐ ┌────▼──┐
              │Instance │ │Instance│ │Instance│
              │  1      │ │  2     │ │  3    │
              │t3.micro │ │t3.micro│ │t3.micro│
              └─────────┘ └────────┘ └────────┘
              
                 Auto Scaling Group
              (Min: 3, Max: 6, Desired: 3)
```

## 🚀 Quick Start

### Prerequisites
- AWS Account with valid credentials
- `packer` installed
- `terraform` installed
- `aws-cli` configured

### 1. Build AMI with Packer

```bash
cd scripts/packer

# Build the AMI
packer build sample-app.pkr.hcl

# Get AMI ID
AMI_ID=$(cat ami-id.txt)
echo "AMI ID: $AMI_ID"
```

### 2. Deploy Infrastructure with Terraform

```bash
cd ../tofu/live/asg-sample

# Initialize Terraform
terraform init

# Plan deployment
terraform plan -out=tfplan

# Apply configuration
terraform apply tfplan

# Get outputs
terraform output
```

### 3. Access Application

```bash
# Get ALB DNS
ALB_DNS=$(terraform output -raw alb_dns_name)

# Test application
curl http://$ALB_DNS

# Open in browser
echo "http://$ALB_DNS"
```

## 📁 Project Structure

```
TD3/
├── scripts/
│   ├── packer/
│   │   ├── sample-app.pkr.hcl      # Packer configuration
│   │   ├── app.js                  # Node.js application
│   │   ├── app.config.js           # PM2 ecosystem config
│   │   ├── manifest.json           # Build artifacts
│   │   └── ami-id.txt              # Generated AMI ID
│   │
│   └── tofu/
│       └── live/
│           └── asg-sample/
│               ├── main.tf         # Main infrastructure
│               ├── variables.tf    # Variable definitions
│               ├── outputs.tf      # Output definitions
│               ├── terraform.tfvars # Variable values
│               ├── terraform.tfstate # State (local)
│               └── .terraform/     # Provider plugins
│
├── DEPLOYMENT.md                   # Detailed deployment guide
└── README.md                       # This file
```

## 🔧 Components

### Packer
- **Base Image**: Amazon Linux 2023
- **Runtime**: Node.js 18.20.8 LTS
- **Process Manager**: PM2 6.0.14
- **User**: app-user (dedicated)
- **Build Time**: ~6 minutes

### Terraform
- **VPC**: Default
- **ALB**: Application Load Balancer
- **ASG**: Auto Scaling Group (3 instances)
- **Instance Type**: t3.micro
- **Region**: us-east-2

### Application
- **Framework**: Node.js with Express
- **Port**: 8080
- **Endpoint**: GET /
- **Response**: `{"message": "Hello from Node.js app!"}`

## 📊 Monitoring & Testing

### Check Application Status

```bash
# Get ALB DNS
ALB_DNS=$(aws elbv2 describe-load-balancers \
  --names sample-app-alb \
  --query "LoadBalancers[0].DNSName" \
  --output text \
  --region us-east-2)

# Test application
curl http://$ALB_DNS

# Check instances
aws ec2 describe-instances \
  --filters "Name=tag:aws:autoscaling:groupName,Values=sample-app-asg" \
  --region us-east-2

# Check ASG
aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names sample-app-asg \
  --region us-east-2

# Check target health
aws elbv2 describe-target-health \
  --target-group-arn <TARGET_GROUP_ARN> \
  --region us-east-2
```

## 💰 Cost Estimate

| Resource | Type | Monthly Cost |
|----------|------|--------------|
| EC2 | 3x t3.micro | ~$3 |
| ALB | Application LB | ~$15 |
| Data Transfer | Minimal | ~$0-1 |
| **Total** | | **~$20/month** |

(Prices vary by region and usage)

## 🧹 Cleanup

To destroy all resources:

```bash
cd scripts/tofu/live/asg-sample

# Destroy infrastructure
terraform destroy -auto-approve

# Deregister AMI
aws ec2 deregister-image \
  --image-id ami-093653d8864441a75 \
  --region us-east-2

# Delete snapshots (optional)
aws ec2 describe-snapshots \
  --owner-ids self \
  --region us-east-2
```

## 📝 Logs & Debugging

### View Application Logs
```bash
# SSH into instance (if needed)
# aws ec2-instance-connect send-ssh-public-key...

# Or view via Systems Manager Session Manager
aws ssm start-session --target <instance-id> --region us-east-2
```

### Terraform Logs
```bash
# Enable debug logging
export TF_LOG=DEBUG
terraform plan

# Save to file
export TF_LOG_PATH=./terraform.log
```

## ✅ Verification Checklist

- [x] Packer build successful (AMI created)
- [x] Terraform initialization successful
- [x] ALB deployed and active
- [x] ASG deployed with 3 instances
- [x] All instances healthy
- [x] Application accessible via HTTP
- [x] Load balancing working
- [x] Auto-scaling configured

## 🔗 Resources

- [Packer Documentation](https://www.packer.io/docs)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [AWS ALB Documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/)

## 📧 Support

For issues or questions, check:
1. DEPLOYMENT.md (detailed guide)
2. Terraform logs (TF_LOG)
3. AWS CloudWatch logs
4. Application logs (PM2 logs)

---

**Status**: ✅ Production Ready  
**Last Updated**: December 4, 2025  
**Region**: us-east-2
