# Configuration CI/CD Permissions

Cette configuration déploie le fournisseur OIDC GitHub et les rôles IAM pour GitHub Actions.

## Prérequis

- AWS CLI configuré
- OpenTofu/Terraform installé
- Accès AWS avec permissions pour créer IAM roles

## Déploiement

```bash
# Initialiser
tofu init

# Planifier
tofu plan

# Appliquer
tofu apply

# Afficher les sorties
tofu output
```

## Sorties

- `oidc_provider_arn` - ARN du fournisseur OIDC
- `lambda_test_role_arn` - ARN du rôle de test
- `lambda_deploy_plan_role_arn` - ARN du rôle de plan
- `lambda_deploy_apply_role_arn` - ARN du rôle d'apply

## Secrets GitHub

Copier les valeurs de sortie dans GitHub Settings → Secrets:

```
OIDC_ROLE_ARN_TEST = lambda_test_role_arn
OIDC_ROLE_ARN_PLAN = lambda_deploy_plan_role_arn
OIDC_ROLE_ARN_APPLY = lambda_deploy_apply_role_arn
AWS_REGION = us-east-2
```
