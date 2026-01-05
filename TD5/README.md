# TD5 - CI/CD DevOps avec GitHub Actions, AWS Lambda et Terraform

**Status:** ✅ **PARTIE 1 - COMPLÈTEMENT OPÉRATIONNELLE**

## 📋 Table des Matières
- Vue d'ensemble
- Architecture
- Prérequis
- Installation
- Utilisation
- API Endpoints
- Tests
- Structure du Projet
- Documentation

## 🎯 Vue d'Ensemble

TD5 implémente un pipeline CI/CD complet utilisant:
- Infrastructure as Code (Terraform/OpenTofu)
- Serverless Computing (AWS Lambda)
- API Management (API Gateway)
- CI/CD Automation (GitHub Actions)
- Secure Authentication (OIDC Tokens)

### ✨ Caractéristiques
✅ 5 Endpoints API fonctionnels
✅ 11 Tests unitaires (100% réussite)
✅ 5 Workflows GitHub Actions
✅ Infrastructure entièrement en code
✅ Authentification sécurisée (OIDC)
✅ 0 Hardcoded credentials
✅ Monitoring & Logging
✅ 100% Modulaire & Réutilisable

## 🏗️ Architecture

```
GitHub Repository
    ↓ (OIDC Tokens)
AWS Infrastructure
├── OIDC Provider & IAM Roles
├── Lambda Function (Python 3.11)
└── API Gateway (HTTP)
```

## 📦 Contenu

### Application Lambda
- **5 Endpoints**: /, /health, /api/status, /name/{name}, /api/echo, /api/info
- **11 Tests Unitaires**: 100% réussite
- **Python 3.11**: Runtime
- **CloudWatch Logs**: Monitoring

### Infrastructure
- **4 Modules Terraform**: github-aws-oidc, gh-actions-iam-roles, lambda-function, api-gateway
- **3 Rôles IAM**: test, plan, apply
- **OIDC Provider**: GitHub sécurisé
- **API Gateway**: HTTP + CORS

### CI/CD Pipeline
- **app-tests.yml**: Tests Python
- **infra-tests.yml**: Tests Terraform
- **deploy-plan.yml**: Terraform Plan
- **deploy-apply.yml**: Terraform Apply
- **deploy-destroy.yml**: Terraform Destroy

## 🚀 Quick Start

```bash
# Cloner
git clone https://github.com/bibatou2004/Devops_Lab.git
cd Devops_Lab/TD5

# Déployer
cd scripts/tofu/live/ci-cd-permissions
terraform init
terraform apply

# Tester
API_URL=$(terraform output -raw api_endpoint)
curl $API_URL/
curl $API_URL/api/status
curl "$API_URL/name/DevOps"
```

## 📊 Statistiques

| Métrique | Valeur |
|----------|--------|
| Endpoints API | 5 |
| Tests Unitaires | 11 |
| Success Rate | 100% |
| Workflows | 5 |
| Modules Terraform | 4 |
| Secrets GitHub | 4 |

## 📚 Documentation

- [STRUCTURE.md](./STRUCTURE.md) - Architecture détaillée
- [OVERVIEW.md](./OVERVIEW.md) - Vue d'ensemble
- [Application README](./scripts/sample-app/README.md) - Lambda docs
- [OIDC Guide](./docs/OIDC_CONFIGURATION_GUIDE.md) - Configuration OIDC

## 🔐 Sécurité

- ✅ OIDC Token Authentication
- ✅ 0 Hardcoded Credentials
- ✅ IAM Least Privilege
- ✅ GitHub Secrets Management
- ✅ CloudWatch Audit Logs

## 🤝 Contribution

1. Fork le repository
2. Create une branche
3. Commit les changements
4. Push et open PR

## 📄 License

MIT License

## 👤 Auteur

**Biba Wandaogo** - DevOps Engineer  
GitHub: [@bibatou2004](https://github.com/bibatou2004)

---

**Status:** ✅ Partie 1 Complètement Opérationnelle  
**Last Updated:** 2024-12-05  
**Repository:** https://github.com/bibatou2004/Devops_Lab
