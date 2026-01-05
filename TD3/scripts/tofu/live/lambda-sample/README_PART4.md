# Part 4: Serverless Orchestration with AWS Lambda 🚀

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Part 4.1: Create Lambda Function](#part-41-create-lambda-function)
4. [Part 4.2: Deploy with Terraform](#part-42-deploy-with-terraform)
5. [Part 4.3: API Gateway Integration](#part-43-api-gateway-integration)
6. [Part 4.4: Update and Re-Deploy](#part-44-update-and-re-deploy)
7. [Project Structure](#project-structure)
8. [Cleanup](#cleanup)
9. [Conclusion](#conclusion)

---

## 📖 Overview

In this part, we explore **serverless orchestration** using AWS Lambda and API Gateway. We'll:

- Create a serverless function using AWS Lambda
- Deploy infrastructure as code with Terraform/OpenTofu
- Configure API Gateway to trigger Lambda functions
- Implement rapid updates without managing servers
- Understand the benefits of serverless architecture

**Key Learning Outcomes:**
- ✅ Serverless function deployment
- ✅ Infrastructure as Code (IaC) with Terraform
- ✅ API Gateway integration
- ✅ Rapid deployment cycles
- ✅ AWS resource management

---

## 🔧 Prerequisites

### Required Tools

```bash
# AWS CLI
aws --version
# AWS CLI 2.x or higher

# Terraform
terraform version
# Terraform v1.6.6 or higher

# Node.js (for local development)
node --version
# Node.js 20.x or higher

# Git
git --version
```

### AWS Setup

```bash
# Configure AWS credentials
aws configure
# AWS Access Key ID: [your-key]
# AWS Secret Access Key: [your-secret-key]
# Default region: us-east-2
# Default output format: json

# Verify credentials
aws sts get-caller-identity
```

---

## 📦 Part 4.1: Create Lambda Function

### Step 1.1: Set Up Working Directory

```bash
mkdir -p devops_base/TD3/scripts/tofu/live/lambda-sample/src
cd devops_base/TD3/scripts/tofu/live/lambda-sample
```

### Step 1.2: Create Lambda Function Code

**File: `src/index.js` (Version 1)**

```javascript
exports.handler = (event, context, callback) => {
  callback(null, { statusCode: 200, body: "Hello, World!" });
};
```

### Step 1.3: Create Terraform Modules

**Module: `modules/lambda/main.tf`**

```hcl
resource "aws_lambda_function" "this" {
  filename         = data.archive_file.this.output_path
  function_name    = var.name
  role             = aws_iam_role.this.arn
  handler          = var.handler
  runtime          = var.runtime
  memory_size      = var.memory_size
  timeout          = var.timeout
  source_code_hash = data.archive_file.this.output_base64sha256
  
  environment {
    variables = var.environment_variables
  }
}
```

**Module: `modules/api-gateway/main.tf`**

```hcl
resource "aws_apigatewayv2_api" "this" {
  name          = var.name
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "this" {
  api_id             = aws_apigatewayv2_api.this.id
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
  integration_uri    = var.function_arn
}
```

---

## ☸️ Part 4.2: Deploy with Terraform

### Step 2.1: Create Main Configuration

**File: `main.tf`**

```hcl
provider "aws" {
  region = "us-east-2"
}

module "function" {
  source = "../modules/lambda"
  
  name              = "lambda-sample"
  src_dir           = "${path.module}/src"
  runtime           = "nodejs20.x"
  handler           = "index.handler"
  memory_size       = 128
  timeout           = 5
  
  environment_variables = {
    NODE_ENV = "production"
  }
}

module "gateway" {
  source = "../modules/api-gateway"
  
  name            = "lambda-sample"
  function_arn    = module.function.function_arn
  function_name   = module.function.function_name
}
```

### Step 2.2: Initialize Terraform

```bash
cd lambda-sample

terraform init
terraform validate
terraform plan
```

### Step 2.3: Deploy Infrastructure

```bash
terraform apply

# Type 'yes' when prompted
```

**Expected Output:**
```
Apply complete! Resources: 8 added, 0 changed, 0 destroyed.

Outputs:
api_endpoint = "https://xxxxxxxxxx.execute-api.us-east-2.amazonaws.com/"
lambda_function_name = "lambda-sample"
```

---

## 🌐 Part 4.3: API Gateway Integration

### Step 3.1: Test the API Endpoint

```bash
# Retrieve endpoint
API_ENDPOINT=$(terraform output -raw api_endpoint)

# Test
curl -s "$API_ENDPOINT"

# Expected Output:
# Hello, World!
```

### Step 3.2: Verify in AWS Console

1. Open [AWS Lambda Console](https://console.aws.amazon.com/lambda/)
2. Find function: `lambda-sample`
3. Check status: ✅ Active
4. View configuration: ✅ Correct

---

## 🔄 Part 4.4: Update and Re-Deploy

### Step 4.1: Update Lambda Function Code

**File: `src/index.js` (Version 2)**

```javascript
exports.handler = (event, context, callback) => {
  callback(null, { statusCode: 200, body: "🚀 DevOps Base v2 - Serverless!" });
};
```

### Step 4.2: Re-Deploy

```bash
terraform apply

# Type 'yes' when prompted
```

### Step 4.3: Test Updated Version

```bash
API_ENDPOINT=$(terraform output -raw api_endpoint)

curl -s "$API_ENDPOINT"

# Expected Output:
# 🚀 DevOps Base v2 - Serverless!
```

---

## 📁 Project Structure

```
devops_base/TD3/scripts/tofu/live/
├── lambda-sample/
│   ├── src/
│   │   └── index.js              (v1 & v2)
│   ├── main.tf                   (Lambda + API Gateway config)
│   ├── outputs.tf                (API endpoint output)
│   ├── terraform.tfstate         (State file)
│   ├── terraform.tfvars          (Variables - if needed)
│   └── README_PART4.md           (This file)
├── modules/
│   ├── lambda/
│   │   ├── main.tf               (Lambda resource)
│   │   ├── variables.tf          (Lambda variables)
│   │   └── outputs.tf            (Lambda outputs)
│   └── api-gateway/
│       ├── main.tf               (API Gateway resource)
│       ├── variables.tf          (API Gateway variables)
│       └── outputs.tf            (API Gateway outputs)
└── ...
```

---

## 🛠️ Technologies Used

- **AWS Lambda**: Serverless compute service
- **API Gateway**: HTTP API management
- **Terraform**: Infrastructure as Code
- **Node.js**: Lambda runtime (nodejs20.x)
- **IAM**: Identity and Access Management

---

## 💰 Cost Estimation

| Resource | Cost | Status |
|----------|------|--------|
| **Lambda** | $0.20 per 1M requests | ✅ FREE TIER |
| **API Gateway** | $3.50 per million API calls | ✅ FREE TIER |
| **Data Transfer** | $0.09 per GB | ✅ Small usage |
| **Total (Test)** | ~$0 | ✅ FREE TIER |

**Note:** AWS Free Tier includes 1M Lambda invocations/month and 1M API Gateway calls/month.

---

## 🧹 Cleanup

### Step 1: Destroy AWS Resources

```bash
cd lambda-sample

terraform destroy

# Type 'yes' when prompted
```

### Step 2: Verify Deletion

```bash
# Check Lambda Console
# - lambda-sample function should be deleted

# Check API Gateway Console
# - lambda-sample API should be deleted

# Check IAM Console
# - lambda-sample-role should be deleted
```

### Step 3: Clean Local Files

```bash
# Remove Terraform state files
rm -rf .terraform .terraform.lock.hcl terraform.tfstate*

# Or keep for version control
git add terraform.tfstate*
```

---

## 📊 Key Metrics

### Deployment Time
- **Initial Deploy**: ~30-45 seconds
- **Update Deploy**: ~5-10 seconds
- **Destruction**: ~20-30 seconds

### Serverless Benefits
- ✅ No server management
- ✅ Auto-scaling
- ✅ Pay-as-you-go pricing
- ✅ Rapid deployment
- ✅ Built-in monitoring

### Serverless Limitations
- ⚠️ Cold start latency
- ⚠️ Execution time limits (15 min for Lambda)
- ⚠️ Memory constraints
- ⚠️ Stateless functions

---

## 📚 Learning Outcomes

By completing Part 4, you've learned:

✅ **Serverless Architecture**
- Deploy functions without managing servers
- Understand event-driven computing
- Scale automatically with demand

✅ **Infrastructure as Code**
- Write Terraform configurations
- Manage AWS resources declaratively
- Version control infrastructure

✅ **API Integration**
- Connect Lambda to API Gateway
- Handle HTTP requests
- Return JSON responses

✅ **Rapid Deployment**
- Update code instantly
- Deploy in seconds
- Zero infrastructure downtime

---

## 🎯 Exercises

To deepen your understanding, try:

1. **Add Error Handling**
   - Modify Lambda to catch errors
   - Return appropriate HTTP status codes
   - Add logging for debugging

2. **Add Environment Variables**
   - Use environment variables in Lambda
   - Deploy different versions (dev/prod)
   - Manage secrets securely

3. **Add Database Integration**
   - Connect Lambda to DynamoDB
   - Store/retrieve data
   - Implement CRUD operations

4. **Add Authentication**
   - Implement API authentication
   - Use AWS Cognito
   - Secure endpoints

---

## ✅ Testing Checklist

- [ ] AWS credentials configured
- [ ] Terraform installed and working
- [ ] Lambda function created
- [ ] API Gateway deployed
- [ ] API endpoint accessible
- [ ] Initial test passes (v1)
- [ ] Code updated (v2)
- [ ] Re-deployment successful
- [ ] Updated version accessible
- [ ] All resources destroyed
- [ ] No orphaned AWS resources

---

## 🚀 Next Steps

### After Part 4

1. **Continue with Infrastructure:**
   - Add more Lambda functions
   - Create microservices architecture
   - Implement event-driven patterns

2. **Add Monitoring:**
   - CloudWatch logs
   - Performance metrics
   - Alert configuration

3. **Secure Your API:**
   - API authentication
   - Rate limiting
   - CORS configuration

4. **Move to Part 5:**
   - Explore other serverless services
   - AWS Step Functions
   - EventBridge integration

---

## 📖 Additional Resources

- **AWS Lambda**: https://aws.amazon.com/lambda/
- **API Gateway**: https://aws.amazon.com/api-gateway/
- **Terraform AWS Provider**: https://registry.terraform.io/providers/hashicorp/aws/latest/docs
- **Serverless Framework**: https://www.serverless.com/
- **AWS Free Tier**: https://aws.amazon.com/free/

---

## 📝 Troubleshooting

### Problem: "No changes" detected after code update

**Solution:**
```hcl
# Add source_code_hash to trigger updates
source_code_hash = data.archive_file.this.output_base64sha256
```

### Problem: API Gateway returns 502 error

**Solution:**
- Check Lambda execution role permissions
- Verify Lambda function code
- Check CloudWatch logs for errors

### Problem: Terraform destroy fails

**Solution:**
```bash
# Force destroy with -auto-approve
terraform destroy -auto-approve
```

---

## 📊 Deployment Flow

```
Code Update
    ↓
git push
    ↓
terraform apply
    ↓
Archive code
    ↓
Upload to Lambda
    ↓
Update function
    ↓
API Gateway routes request
    ↓
Lambda executes
    ↓
Response returned (~100-500ms)
```

---

## 🎉 Conclusion

In Part 4, you've successfully:

✅ **Created a serverless function** using AWS Lambda  
✅ **Deployed infrastructure** using Terraform  
✅ **Integrated API Gateway** for HTTP access  
✅ **Updated and re-deployed** code rapidly  
✅ **Understood serverless benefits** and limitations  
✅ **Managed costs** with AWS Free Tier  

You're now ready for **Part 5: Advanced Serverless Patterns** or **Production Deployment**!

---

**Last Updated**: December 5, 2025  
**Status**: ✅ Complete and Tested  
**Version**: 1.0  
**AWS Region**: us-east-2

