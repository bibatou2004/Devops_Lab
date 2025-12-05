# Section 7 : Modules OpenTofu depuis GitHub

## 📚 Vue d'ensemble

Utilisation de modules réutilisables depuis GitHub avec versioning.

## Exercise 11 : Versioning des modules

### Option 1 : Utiliser un Git tag

```hcl
module "sample_app" {
  source = "github.com/bibatou2004/Devops_Lab.git//TD3/scripts/tofu/modules/ec2-instance?ref=v1.0.0"
  
  ami_id = var.ami_id
  name   = "sample-app-v1"
}
```

### Option 2 : Utiliser un commit spécifique

```hcl
module "sample_app" {
  source = "github.com/bibatou2004/Devops_Lab.git//TD3/scripts/tofu/modules/ec2-instance?ref=abc123def456"
  
  ami_id = var.ami_id
  name   = "sample-app-commit"
}
```

### Option 3 : Utiliser une branche

```hcl
module "sample_app" {
  source = "github.com/bibatou2004/Devops_Lab.git//TD3/scripts/tofu/modules/ec2-instance?ref=main"
  
  ami_id = var.ami_id
  name   = "sample-app-main"
}
```

## Implémentation

### Étape 1 : Créer un Git tag

```bash
cd /home/bibawandaogo/Devops_Lab

git tag v1.0.0
git push origin v1.0.0
```

### Étape 2 : Utiliser le tag dans main.tf

```hcl
module "sample_app" {
  source = "github.com/bibatou2004/Devops_Lab.git//TD3/scripts/tofu/modules/ec2-instance?ref=v1.0.0"
  
  ami_id              = "ami-0dc529b866af9ec38"
  instance_count      = 2
  app_name            = "sample-app-v1"
}
```

### Étape 3 : Déployer

```bash
terraform init
terraform apply
```

## Avantages du versioning

✅ **Stabilité** : Version précise du module
✅ **Traçabilité** : Savoir quelle version est en prod
✅ **Rollback** : Facile de revenir à une ancienne version
✅ **CI/CD** : Pipeline automatisé

## Exercise 12 : Utiliser un module du Registry

### Exemple : Module VPC du Registry

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-2a", "us-east-2b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  enable_vpn_gateway = true

  tags = {
    Environment = "prod"
  }
}
```

### Utiliser dans notre configuration

```bash
cd /home/bibawandaogo/devops_base/TD3/scripts/tofu/ec2-with-modules

# Modifier main.tf pour ajouter le VPC
cat >> main.tf << 'EOF'

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "sample-app-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-2a", "us-east-2b"]
  public_subnets = ["10.0.1.0/24", "10.0.2.0/24"]

  enable_nat_gateway = false

  tags = {
    Name = "sample-app-vpc"
  }
}

# Utiliser le VPC dans notre module
module "sample_app" {
  source = "../modules/ec2-instance"

  ami_id               = var.ami_id
  instance_count       = var.instance_count
  instance_type        = var.instance_type
  name                 = var.app_name
  security_group_name  = var.security_group_name
  environment          = var.environment
}
