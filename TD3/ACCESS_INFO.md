# Application Access Information

## 🌐 Application URL

To get the current ALB DNS name:

```bash
aws elbv2 describe-load-balancers \
  --names sample-app-alb \
  --query "LoadBalancers[0].DNSName" \
  --output text \
  --region us-east-2
```

### Current Application URL
```
http://sample-app-alb-935dd84773deedec.us-east-2.elb.amazonaws.com
```

## 📊 AWS Resources

### Load Balancer
- **Name**: sample-app-alb
- **Type**: Application Load Balancer
- **Protocol**: HTTP
- **Port**: 80
- **Region**: us-east-2

### Auto Scaling Group
- **Name**: sample-app-asg
- **Min Size**: 3
- **Max Size**: 6
- **Desired**: 3
- **Instance Type**: t3.micro

### Target Group
- **Name**: sample-app-tg
- **Protocol**: HTTP
- **Port**: 8080
- **Health Check Path**: /

## 🧪 Testing

### Simple Test
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

### Load Testing (10 requests)
```bash
for i in {1..10}; do
  curl -s http://$ALB_DNS
  echo "✅ Request $i"
done
```

## 📊 Monitoring

### Check Instance Status
```bash
aws ec2 describe-instances \
  --filters "Name=tag:aws:autoscaling:groupName,Values=sample-app-asg" \
  --query "Reservations[].Instances[].[InstanceId,State.Name,LaunchTime]" \
  --output table \
  --region us-east-2
```

### Check Target Health
```bash
TG_ARN=$(aws elbv2 describe-target-groups \
  --names sample-app-tg \
  --query "TargetGroups[0].TargetGroupArn" \
  --output text \
  --region us-east-2)

aws elbv2 describe-target-health \
  --target-group-arn $TG_ARN \
  --region us-east-2
```

### Check ALB Status
```bash
aws elbv2 describe-load-balancers \
  --names sample-app-alb \
  --query "LoadBalancers[0].[LoadBalancerName,DNSName,State.Code]" \
  --output table \
  --region us-east-2
```

## 🔐 Security Groups

### ALB Security Group
- **Name**: sample-app-alb-sg
- **Inbound**: 80 from 0.0.0.0/0
- **Outbound**: All traffic

### Instance Security Group
- **Name**: sample-app-sg
- **Inbound**: 8080 from ALB SG
- **Outbound**: All traffic

## 💾 Backup Information

### AMI Details
- **AMI ID**: ami-093653d8864441a75
- **Name**: packer-sample-app-1764867129
- **OS**: Amazon Linux 2023
- **Region**: us-east-2

### State Files
- Terraform state: `scripts/tofu/live/asg-sample/terraform.tfstate`
- State backup: `scripts/tofu/live/asg-sample/terraform.tfstate.backup`

## 🔄 Deployment History

| Date | Action | Status |
|------|--------|--------|
| 2025-12-04 | Packer Build | ✅ Success |
| 2025-12-04 | Terraform Init | ✅ Success |
| 2025-12-04 | Infrastructure Deploy | ✅ Success |
| 2025-12-04 | Application Test | ✅ Success |

