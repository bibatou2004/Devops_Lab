# 🔐 Configuration OIDC avec AWS et GitHub Actions

## Vue d'ensemble

OIDC (OpenID Connect) permet à GitHub Actions de s'authentifier auprès d'AWS sans stockage de credentials longue durée. C'est plus sécurisé que les clés d'accès statiques.

## Avantages OIDC vs Machine User

| Aspect | OIDC | Machine User |
|--------|------|-------------|
| Sécurité | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Durée de vie | Courte (15 min) | Longue (mois/années) |
| Gestion | Automatique | Manuel |
| Rotation | Chaque exécution | Manual |
| Coût | Gratuit | Compte AWS |

## Configuration Étape par Étape

### Étape 1: Préparer la Structure

```bash
cd /home/bibawandaogo/TD4/devops-lab/TD5

mkdir -p scripts/tofu/modules/github-aws-oidc
cd scripts/tofu/modules/github-aws-oidc
```

### Étape 2: Créer le Module OIDC

**Fichier: `versions.tf`**

```hcl
terraform {
  required_version = ">= 1.0"

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
```

**Fichier: `variables.tf`**

```hcl
variable "aws_region" {
  description = "Région AWS"
  type        = string
  default     = "us-east-2"
}

variable "provider_url" {
  description = "URL du fournisseur OIDC GitHub"
  type        = string
  default     = "https://token.actions.githubusercontent.com"
}

variable "audience" {
  description = "Audience OIDC"
  type        = string
  default     = "sts.amazonaws.com"
}
```

**Fichier: `main.tf`**

```hcl
# Créer le fournisseur OIDC dans AWS
resource "aws_iam_openid_connect_provider" "github" {
  url             = var.provider_url
  client_id_list  = [var.audience]
  thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]

  tags = {
    Name = "github-oidc-provider"
  }
}

# Afficher l'ARN du fournisseur
output "oidc_provider_arn" {
  value = aws_iam_openid_connect_provider.github.arn
}
```

**Fichier: `outputs.tf`**

```hcl
output "oidc_provider_arn" {
  description = "ARN du fournisseur OIDC GitHub"
  value       = aws_iam_openid_connect_provider.github.arn
}

output "oidc_provider_url" {
  description = "URL du fournisseur OIDC"
  value       = aws_iam_openid_connect_provider.github.url
}
```

### Étape 3: Créer le Module Rôles IAM

```bash
mkdir -p ../gh-actions-iam-roles
cd ../gh-actions-iam-roles
```

**Fichier: `variables.tf`**

```hcl
variable "oidc_provider_arn" {
  description = "ARN du fournisseur OIDC GitHub"
  type        = string
}

variable "github_repo" {
  description = "Dépôt GitHub (format: owner/repo)"
  type        = string
}

variable "name" {
  description = "Nom de base pour les rôles IAM"
  type        = string
  default     = "github-actions"
}

variable "enable_iam_role_for_testing" {
  description = "Créer le rôle IAM pour les tests"
  type        = bool
  default     = true
}

variable "enable_iam_role_for_plan" {
  description = "Créer le rôle IAM pour le plan"
  type        = bool
  default     = true
}

variable "enable_iam_role_for_apply" {
  description = "Créer le rôle IAM pour l'apply"
  type        = bool
  default     = true
}
```

**Fichier: `main.tf` (Rôle de Test)**

```hcl
# Politique de confiance pour OIDC
data "aws_iam_policy_document" "github_oidc_trust" {
  statement {
    effect = "Allow"

    principals {
      type        = "Federated"
      identifiers = [var.oidc_provider_arn]
    }

    action = "sts:AssumeRoleWithWebIdentity"

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_repo}:*"]
    }
  }
}

# Rôle pour les tests
resource "aws_iam_role" "github_test_role" {
  count              = var.enable_iam_role_for_testing ? 1 : 0
  name               = "${var.name}-test-role"
  assume_role_policy = data.aws_iam_policy_document.github_oidc_trust.json

  tags = {
    Name = "github-test-role"
  }
}

# Politique pour les tests
resource "aws_iam_role_policy" "github_test_policy" {
  count  = var.enable_iam_role_for_testing ? 1 : 0
  name   = "${var.name}-test-policy"
  role   = aws_iam_role.github_test_role[0].id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "lambda:*",
          "apigateway:*",
          "iam:GetRole",
          "iam:PassRole",
          "logs:*"
        ]
        Resource = "*"
      }
    ]
  })
}

# Rôle pour le plan
resource "aws_iam_role" "github_plan_role" {
  count              = var.enable_iam_role_for_plan ? 1 : 0
  name               = "${var.name}-plan-role"
  assume_role_policy = data.aws_iam_policy_document.github_oidc_trust.json

  tags = {
    Name = "github-plan-role"
  }
}

# Rôle pour l'apply
resource "aws_iam_role" "github_apply_role" {
  count              = var.enable_iam_role_for_apply ? 1 : 0
  name               = "${var.name}-apply-role"
  assume_role_policy = data.aws_iam_policy_document.github_oidc_trust.json

  tags = {
    Name = "github-apply-role"
  }
}
```

**Fichier: `outputs.tf`**

```hcl
output "lambda_test_role_arn" {
  value = var.enable_iam_role_for_testing ? aws_iam_role.github_test_role[0].arn : null
}

output "lambda_deploy_plan_role_arn" {
  value = var.enable_iam_role_for_plan ? aws_iam_role.github_plan_role[0].arn : null
}

output "lambda_deploy_apply_role_arn" {
  value = var.enable_iam_role_for_apply ? aws_iam_role.github_apply_role[0].arn : null
}
```

### Étape 4: Créer la Configuration Live

```bash
mkdir -p ../../../live/ci-cd-permissions
cd ../../../live/ci-cd-permissions
```

**Fichier: `main.tf`**

```hcl
provider "aws" {
  region = "us-east-2"  # Remplacez par votre région
}

module "oidc_provider" {
  source = "../../modules/github-aws-oidc"
}

module "iam_roles" {
  source = "../../modules/gh-actions-iam-roles"

  oidc_provider_arn = module.oidc_provider.oidc_provider_arn
  github_repo       = "bibatou2004/Devops_Lab"  # Remplacez par votre repo
  
  name                            = "lambda-sample"
  enable_iam_role_for_testing     = true
  enable_iam_role_for_plan        = true
  enable_iam_role_for_apply       = true
}
```

**Fichier: `outputs.tf`**

```hcl
output "lambda_test_role_arn" {
  value = module.iam_roles.lambda_test_role_arn
}

output "lambda_deploy_plan_role_arn" {
  value = module.iam_roles.lambda_deploy_plan_role_arn
}

output "lambda_deploy_apply_role_arn" {
  value = module.iam_roles.lambda_deploy_apply_role_arn
}
```

### Étape 5: Déployer OIDC & IAM

```bash
cd /home/bibawandaogo/TD4/devops-lab/TD5/scripts/tofu/live/ci-cd-permissions

tofu init

tofu plan

tofu apply

# Afficher les sorties
tofu output
```

### Étape 6: Copier les ARNs

Notez les trois ARNs:
- `lambda_test_role_arn`
- `lambda_deploy_plan_role_arn`
- `lambda_deploy_apply_role_arn`

Vous en aurez besoin pour les secrets GitHub.

---

## Configuration GitHub Secrets

### Aller à GitHub

1. Allez à votre dépôt: https://github.com/YOUR_USERNAME/Devops_Lab
2. Settings → Secrets and variables → Actions
3. Créer les secrets suivants:

**Secret 1: OIDC_ROLE_ARN_TEST**
```
arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-sample-test-role
```

**Secret 2: OIDC_ROLE_ARN_PLAN**
```
arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-sample-plan-role
```

**Secret 3: OIDC_ROLE_ARN_APPLY**
```
arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-sample-apply-role
```

**Secret 4: AWS_REGION**
```
us-east-2
```

---

## Vérification

Pour vérifier la configuration OIDC:

```bash
# Dans AWS CLI
aws iam list-open-id-connect-providers

# Vérifier le certificat du fournisseur
aws iam get-open-id-connect-provider \
  --open-id-connect-provider-arn arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com
```

---

## Dépannage

### Erreur: "ValidationError: Invalid length for parameter ThumbprintList"

Utilisez le thumbprint correct: `6938fd4d98bab03faadb97b34396831e3780aea1`

### Erreur: "NotFound: No OIDC provider found"

Assurez-vous que le module OIDC est déployé avant le module IAM.

### OIDC Token Errors

Vérifiez que:
- `github_repo` correspond au format `owner/repo`
- Les rôles IAM permettent `sts:AssumeRoleWithWebIdentity`
- Les secrets GitHub sont correctement configurés

