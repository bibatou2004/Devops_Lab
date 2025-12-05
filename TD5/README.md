# TD5 - CI/CD DevOps avec GitHub Actions, AWS Lambda et Terraform

**Status:** ✅ **PARTIE 1 - COMPLÈTEMENT OPÉRATIONNELLE**

## 📋 Table des Matières

- [Vue d'ensemble](#vue-densemble)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [API Endpoints](#api-endpoints)
- [Tests](#tests)
- [Déploiement](#déploiement)
- [Structure du Projet](#structure-du-projet)
- [Documentation](#documentation)

---

## 🎯 Vue d'Ensemble

**TD5** implémente un pipeline CI/CD complet utilisant:

- **Infrastructure as Code** avec Terraform/OpenTofu
- **Serverless Computing** avec AWS Lambda
- **API Management** avec API Gateway
- **CI/CD Automation** avec GitHub Actions
- **Secure Authentication** avec OIDC Tokens

### ✨ Caractéristiques Principales

✅ **5 Endpoints API** fonctionnels  
✅ **11 Tests unitaires** (100% réussite)  
✅ **5 Workflows GitHub Actions** automatisés  
✅ **Infrastructure entièrement en code** (Terraform)  
✅ **Authentification sécurisée** (OIDC tokens)  
✅ **0 Hardcoded credentials**  
✅ **Monitoring & Logging** complets  
✅ **100% Modulaire & Réutilisable**  

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   GitHub Repository                      │
│  ┌──────────────────────────────────────────────────┐   │
│  │         GitHub Actions Workflows                  │   │
│  │  ✓ app-tests.yml                                 │   │
│  │  ✓ infra-tests.yml                               │   │
│  │  ✓ deploy-plan.yml                               │   │
│  │  ✓ deploy-apply.yml                              │   │
│  │  ✓ deploy-destroy.yml                            │   │
│  └──────────────────────────────────────────────────┘   │
└──────────┬────────────────────────────────────────────┬──┘
           │                                            │
           │ OIDC Token Auth                    Terraform State
           │                                            │
           ▼                                            ▼
┌─────────────────────────────────────────────────────────┐
│              AWS (us-east-2)                            │
│  ┌──────────────────────────────────────────────────┐   │
│  │        OIDC Provider & IAM Roles                 │   │
│  │  ✓ 3 Rôles IAM (test, plan, apply)              │   │
│  │  ✓ Permissions minimales                        │   │
│  └──────────────────────────────────────────────────┘   │
│                       │                                 │
│  ┌────────────────────▼──────────────────────────────┐   │
│  │        Lambda Function (Python 3.11)             │   │
│  │  ✓ 5 Endpoints                                   │   │
│  │  ✓ CloudWatch Logs                              │   │
│  └────────────────────┬──────────────────────────────┘   │
│                       │                                 │
│  ┌────────────────────▼──────────────────────────────┐   │
│  │    API Gateway (HTTP API)                        │   │
│  │  ✓ CORS Enabled                                 │   │
│  │  ✓ Public Endpoint                              │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Prérequis

### Outils Nécessaires

- `terraform` >= 1.0 (ou `tofu`)
- `python` >= 3.11
- `pip` pour les dépendances Python
- `git` configuré
- `gh` (GitHub CLI) authentifié

### Comptes & Credentials

- GitHub account avec accès au repository
- AWS account avec permissions IAM
- GitHub PAT (Personal Access Token) OU OIDC configuré

### Installation des Outils

```bash
# Installer Terraform
sudo apt update
sudo apt install -y terraform

# Installer GitHub CLI
sudo apt install -y gh

# Authentifier GitHub CLI
gh auth login

# Installer Python dependencies
pip install pytest boto3 -q
```

---

## 🚀 Installation

### 1. Cloner le Repository

```bash
git clone https://github.com/bibatou2004/Devops_Lab.git
cd Devops_Lab/TD5
```

### 2. Initialiser Terraform

```bash
cd scripts/tofu/live/ci-cd-permissions

# Initialiser Terraform
terraform init

# Voir le plan
terraform plan

# Appliquer la configuration
terraform apply
```

### 3. Vérifier le Déploiement

```bash
# Récupérer l'URL de l'API
API_URL=$(terraform output -raw api_endpoint)

# Tester les endpoints
curl $API_URL/
curl $API_URL/api/status
curl $API_URL/name/DevOps
```

---

## 💻 Utilisation

### Tester Localement

```bash
cd scripts/sample-app

# Installer les dépendances
pip install -r requirements.txt

# Exécuter les tests
python -m pytest tests/ -v

# Lancer l'application (simulation)
python src/app.py
```

### Tester via API

```bash
# Variables
API_URL=$(cd ../tofu/live/ci-cd-permissions && terraform output -raw api_endpoint)

# Test 1: Health Check
curl $API_URL/

# Test 2: API Status
curl $API_URL/api/status

# Test 3: Greeting
curl "$API_URL/name/DevOps"
curl "$API_URL/name/Biba"

# Test 4: Echo Parameters
curl "$API_URL/api/echo?param1=value1&param2=value2"

# Test 5: API Info
curl $API_URL/api/info
```

---

## 🔌 API Endpoints

### 1. **Health Check**
```
GET /
GET /health

Response:
{
  "status": "healthy",
  "message": "Lambda is running",
  "timestamp": "2024-12-05T..."
}
```

### 2. **API Status**
```
GET /api/status

Response:
{
  "status": "operational",
  "version": "1.0.0",
  "uptime": "...",
  "region": "us-east-2"
}
```

### 3. **Greeting Service**
```
GET /name/{name}

Example: GET /name/DevOps

Response:
{
  "message": "Hello DevOps! Welcome to the API",
  "name": "DevOps",
  "timestamp": "2024-12-05T..."
}
```

### 4. **Echo Service**
```
GET /api/echo?param1=value1&param2=value2

Response:
{
  "message": "Echo service",
  "query_parameters": {
    "param1": "value1",
    "param2": "value2"
  },
  "total_params": 2
}
```

### 5. **API Info**
```
GET /api/info

Response:
{
  "application": "TD5 Sample Lambda",
  "version": "1.0.0",
  "endpoints": [
    "/ or /health - Health check",
    "/api/status - API status",
    "/name/{name} - Greeting with name",
    "/api/echo?param=value - Echo parameters",
    "/api/info - This endpoint"
  ],
  "author": "DevOps Team",
  "created": "2024"
}
```

---

## ✅ Tests

### Exécuter les Tests Unitaires

```bash
cd scripts/sample-app

# Tous les tests
python -m pytest tests/ -v

# Avec couverture
python -m pytest tests/ --cov=src

# Tests spécifiques
python -m pytest tests/test_app.py::TestLambdaHandler::test_health_check_root -v
```

### Tests Disponibles (11 total)

✓ `test_health_check_root` - Vérifier la santé de l'API  
✓ `test_health_check_explicit` - Endpoint /health explicite  
✓ `test_api_status` - Vérifier le statut opérationnel  
✓ `test_name_endpoint_devops` - Greeting avec "DevOps"  
✓ `test_name_endpoint_biba` - Greeting avec "Biba"  
✓ `test_name_endpoint_empty` - Gestion du nom vide  
✓ `test_echo_endpoint` - Service d'écho  
✓ `test_info_endpoint` - Information de l'API  
✓ `test_not_found` - Réponse 404  
✓ `test_response_headers` - Vérifier les headers CORS  
✓ `test_response_is_valid_json` - Validation JSON  

### Résultat des Tests

```
==================================== 11 passed in 0.02s ====================================
```

---

## 🔄 Déploiement

### CI/CD Pipeline - 5 Workflows

#### 1. **Application Tests** (`app-tests.yml`)
- Exécute les tests Python
- Valide la syntaxe
- Génère un rapport de couverture

#### 2. **Infrastructure Tests** (`infra-tests.yml`)
- Valide la configuration Terraform
- Vérifie les modules
- Test la syntaxe HCL

#### 3. **Terraform Plan** (`deploy-plan.yml`)
- Planifie les changements
- Affiche le diff
- Crée un artefact du plan

#### 4. **Terraform Apply** (`deploy-apply.yml`)
- Applique les changements
- Crée les ressources
- Sauvegarde l'état

#### 5. **Terraform Destroy** (`deploy-destroy.yml`)
- Détruit l'infrastructure
- Nettoie les ressources
- Manuel uniquement

### Déclencher un Workflow

```bash
# Les workflows s'exécutent automatiquement on push
git add .
git commit -m "feat: nouvelle feature"
git push origin main

# Vérifier le statut
gh run list --repo bibatou2004/Devops_Lab

# Voir les détails
gh run view <RUN_ID> --log
```

---

## 📁 Structure du Projet

```
TD5/
├── README.md                          # Ce fichier
├── STRUCTURE.md                       # Documentation architecture
├── OVERVIEW.md                        # Vue d'ensemble détaillée
│
├── docs/
│   └── OIDC_CONFIGURATION_GUIDE.md   # Guide OIDC
│
├── scripts/
│   ├── sample-app/                    # Application Lambda
│   │   ├── src/
│   │   │   └── app.py                # Code principal
│   │   ├── tests/
│   │   │   └── test_app.py           # 11 tests unitaires
│   │   ├── README.md
│   │   └── requirements.txt
│   │
│   └── tofu/                          # Infrastructure as Code
│       ├── modules/                   # Modules réutilisables
│       │   ├── github-aws-oidc/       # OIDC Provider
│       │   ├── gh-actions-iam-roles/  # IAM Roles
│       │   ├── lambda-function/       # Lambda Module
│       │   └── api-gateway/           # API Gateway Module
│       │
│       └── live/                      # Configuration Prod
│           └── ci-cd-permissions/
│               ├── main.tf            # Configuration principale
│               ├── variables.tf       # Variables d'entrée
│               ├── outputs.tf         # Outputs
│               └── terraform.tfvars   # Valeurs par défaut
│
└── .github/
    └── workflows/
        ├── app-tests.yml              # Tests Python
        ├── infra-tests.yml            # Tests Terraform
        ├── deploy-plan.yml            # Terraform Plan
        ├── deploy-apply.yml           # Terraform Apply
        └── deploy-destroy.yml         # Terraform Destroy
```

---

## 📚 Documentation

- **[STRUCTURE.md](./STRUCTURE.md)** - Architecture détaillée du projet
- **[OVERVIEW.md](./OVERVIEW.md)** - Vue d'ensemble complète
- **[OIDC_CONFIGURATION_GUIDE.md](./docs/OIDC_CONFIGURATION_GUIDE.md)** - Configuration OIDC
- **[Application README](./scripts/sample-app/README.md)** - Documentation Lambda

---

## 🔐 Sécurité

### OIDC Token Authentication
- ✅ Pas de credentials en dur
- ✅ Tokens temporaires (1 heure)
- ✅ Permissions minimales
- ✅ Audit trail complet

### GitHub Secrets
```
AWS_REGION                 → Region AWS (us-east-2)
OIDC_ROLE_ARN_TEST        → Role pour tests
OIDC_ROLE_ARN_PLAN        → Role pour plan
OIDC_ROLE_ARN_APPLY       → Role pour apply
```

### IAM Roles & Policies
- Role `lambda-test-role` - Permissions pour tests
- Role `lambda-deploy-plan-role` - Terraform plan
- Role `lambda-deploy-apply-role` - Terraform apply

---

## �� Statistiques

| Métrique | Valeur |
|----------|--------|
| Endpoints API | 5 |
| Tests Unitaires | 11 |
| Test Success Rate | 100% |
| Workflows GitHub Actions | 5 |
| Modules Terraform | 4 |
| GitHub Secrets | 4 |
| Lines of Code (App) | ~150 |
| Lines of Code (Tests) | ~200 |
| Lines of Code (Terraform) | ~400 |

---

## 🚀 Prochaines Étapes (Partie 2)

- [ ] Ajouter une base de données (DynamoDB)
- [ ] Implémenter le caching
- [ ] Configurer CloudFront
- [ ] Ajouter du monitoring avancé
- [ ] Implémenter l'autoscaling
- [ ] Ajouter l'authentification API
- [ ] Configurer les alertes
- [ ] Mettre en place le backup

---

## 💡 Commandes Utiles

```bash
# Vérifier l'API
curl https://YOUR_API_ENDPOINT/

# Lister les resources AWS
aws lambda list-functions --region us-east-2
aws apigatewayv2 get-apis --region us-east-2

# Vérifier les logs
aws logs tail /aws/lambda/sample-app --region us-east-2 --follow

# Voir l'état Terraform
cd scripts/tofu/live/ci-cd-permissions
terraform state list
terraform output

# Lancer les tests
cd scripts/sample-app
python -m pytest tests/ -v

# Vérifier les workflows
gh run list --repo bibatou2004/Devops_Lab
```

---

## 🤝 Contribution

1. Fork le repository
2. Create une branche (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Open une Pull Request

---

## 📄 License

MIT License - Voir le fichier LICENSE pour les détails

---

## 👤 Auteur

**Biba Wandaogo**  
DevOps Engineer  
Email: bibatou2004@gmail.com  
GitHub: [@bibatou2004](https://github.com/bibatou2004)

---

## 📞 Support

Pour toute question ou problème:
1. Vérifiez la [documentation](./docs/)
2. Consultez les [issues GitHub](https://github.com/bibatou2004/Devops_Lab/issues)
3. Créez une nouvelle issue si nécessaire

---

**Last Updated:** 2024-12-05  
**Status:** ✅ Partie 1 - Complètement Opérationnelle  
**API Endpoint:** Available in AWS (us-east-2)

