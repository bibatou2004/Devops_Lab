# TD3 - Deployment Complete ✅

## Architecture Overview

```
Internet (0.0.0.0/0)
    ↓ (HTTP 80)
┌─────────────────────┐
│   ALB               │
│ sample-app-alb      │
└──────────┬──────────┘
           ↓ (HTTP 8080)
    ┌──────────────────┐
    │  Target Group    │
    │ sample-app-tg    │
    └─────────┬────────┘
    ┌─────────┴────────┬──────────┬──────────┐
    ↓                  ↓          ↓          ↓
┌────────┐      ┌────────┐  ┌────────┐ ┌────────┐
│Instance│      │Instance│  │Instance│ │Instance│
│  t3:1  │      │  t3:2  │  │  t3:3  │ │Pending │
│ :8080  │      │ :8080  │  │ :8080  │ │(Spare) │
└────────┘      └────────┘  └────────┘ └────────┘
                          
             ASG: sample-app-asg
          Min: 3, Max: 6, Desired: 3
```

## Resources Created

### AMI (Packer)
- **ID**: ami-093653d8864441a75
- **Base**: Amazon Linux 2023
- **Components**:
  - Node.js 18.20.8 LTS
  - npm 10.8.2
  - PM2 6.0.14
  - Application files (app.js, app.config.js)
  - Dedicated app-user

### Infrastructure (Terraform)
- **ALB**: sample-app-alb
  - DNS: `[ALB_DNS_NAME]`
  - Port: 80 (HTTP)
  - Subnets: All AZs

- **ASG**: sample-app-asg
  - Min: 3 instances
  - Max: 6 instances
  - Desired: 3 instances
  - Instance Type: t3.micro
  - AMI: ami-093653d8864441a75

- **Target Group**: sample-app-tg
  - Protocol: HTTP
  - Port: 8080
  - Health Check: /
  - Healthy Threshold: 2
  - Interval: 30s

- **Security Groups**:
  - ALB-SG: Allows 80 from 0.0.0.0/0
  - App-SG: Allows 8080 from ALB-SG

## Testing

### Health Check
```bash
ALB_DNS=$(aws elbv2 describe-load-balancers \
  --names sample-app-alb \
  --query "LoadBalancers[0].DNSName" \
  --output text \
  --region us-east-2)

curl http://$ALB_DNS
```

### Expected Response
```json
{"message": "Hello from Node.js app!"}
```

### Monitoring
```bash
# View ASG
aws autoscaling describe-auto-scaling-groups \
  --auto-scaling-group-names sample-app-asg \
  --region us-east-2

# View Instances
aws ec2 describe-instances \
  --filters "Name=tag:aws:autoscaling:groupName,Values=sample-app-asg" \
  --region us-east-2

# View Load Balancer
aws elbv2 describe-load-balancers \
  --names sample-app-alb \
  --region us-east-2
```

## Cleanup

To destroy all resources:

```bash
cd /home/bibawandaogo/devops_base/TD3/scripts/tofu/live/asg-sample

terraform destroy -auto-approve

# Deregister AMI
aws ec2 deregister-image \
  --image-id ami-093653d8864441a75 \
  --region us-east-2
```

## Summary

| Component | Status | Details |
|-----------|--------|---------|
| AMI Build | ✅ | ami-093653d8864441a75 |
| ALB | ✅ | sample-app-alb |
| ASG | ✅ | 3/3 instances running |
| Application | ✅ | HTTP 200 OK |
| Overall | ✅ | Production Ready |

---

**Deployment Date**: $(date)
**Region**: us-east-2
**Cost Estimate**: ~$5-10/month (t3.micro)
