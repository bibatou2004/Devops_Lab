# 🏗️ Terraform Infrastructure Configuration

Terraform configuration for deploying Lambda functions and API Gateway on AWS.

## 📋 Prerequisites

- Terraform >= 1.0
- AWS credentials configured
- Local provider support (for testing without AWS)

## 🗂️ Files

| File | Purpose |
|------|---------|
| `main.tf` | Main Terraform configuration |
| `deploy.tftest.hcl` | Terraform tests |
| `error-test.tftest.hcl` | Error scenario tests |
| `test.sh` | Automated test script |
| `deployment_template.tpl` | Deployment result template |

## 🚀 Quick Start

```bash
# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Format code
terraform fmt -recursive .

# Create plan
terraform plan -out=tfplan

# Apply configuration
terraform apply tfplan

# Destroy resources
terraform destroy
```

## 🧪 Testing

```bash
# Run automated tests
./test.sh

# Run Terraform tests
terraform test

# Check specific resource
terraform plan -target=local_file.lambda_config
```

## 📊 Generated Files

After `terraform apply`:

- **lambda_config.json** - Lambda function configuration
- **api_config.json** - API Gateway configuration
- **deployment_result.txt** - Deployment summary

## 🔍 Configuration Details

### Lambda Function
- **Runtime**: Node.js 18.x
- **Memory**: 128 MB
- **Timeout**: 30 seconds
- **Handler**: index.handler

### API Gateway
- **Protocol**: HTTP
- **Endpoint**: http://localhost:8080
- **Routes**: 
  - GET /
  - GET /name/{name}
  - GET /add/{a}/{b}

## 📚 Outputs

```bash
terraform output
```

Available outputs:
- `lambda_function_arn`
- `api_endpoint`
- `deployment_file`
- `lambda_config_file`
- `api_config_file`

## 🔧 Troubleshooting

### Issue: Provider not found
```bash
terraform init
```

### Issue: Format errors
```bash
terraform fmt -recursive .
```

### Issue: Validation failed
```bash
terraform validate
```

## 📖 Resources

- [Terraform Docs](https://www.terraform.io/docs/)
- [Local Provider](https://registry.terraform.io/providers/hashicorp/local/latest/docs)
- [AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

## 📄 License

MIT

## 👤 Author

Biba Wandaogo

