# 📁 Structure du Projet TD5

## Hiérarchie Complète

```
TD5/
│
├── README.md                              # Guide principal
├── STRUCTURE.md                           # Ce fichier
├── OVERVIEW.md                            # Navigation rapide
│
├── scripts/
│   ├── sample-app/                        # Application Node.js
│   │   ├── README.md
│   │   ├── app.js
│   │   ├── server.js
│   │   ├── package.json
│   │   ├── jest.config.js
│   │   ├── Dockerfile
│   │   ├── __tests__/
│   │   │   ├── unit/
│   │   │   │   └── app.test.js
│   │   │   └── integration/
│   │   │       └── app.integration.test.js
│   │   └── src/
│   │       └── index.js
│   │
│   └── tofu/                              # Infrastructure OpenTofu
│       ├── modules/
│       │   ├── github-aws-oidc/           # Module OIDC
│       │   │   ├── README.md
│       │   │   ├── main.tf
│       │   │   ├── variables.tf
│       │   │   ├── outputs.tf
│       │   │   └── versions.tf
│       │   │
│       │   ├── gh-actions-iam-roles/      # Module Rôles IAM
│       │   │   ├── README.md
│       │   │   ├── main.tf
│       │   │   ├── variables.tf
│       │   │   ├── outputs.tf
│       │   │   └── versions.tf
│       │   │
│       │   └── lambda/                    # Module Lambda
│       │       ├── main.tf
│       │       ├── variables.tf
│       │       └── outputs.tf
│       │
│       └── live/
│           ├── ci-cd-permissions/         # Configuration OIDC & IAM
│           │   ├── README.md
│           │   ├── main.tf
│           │   ├── variables.tf
│           │   ├── outputs.tf
│           │   ├── terraform.tfvars.example
│           │   └── .gitignore
│           │
│           └── lambda-sample/             # Déploiement Lambda
│               ├── README.md
│               ├── main.tf
│               ├── variables.tf
│               ├── outputs.tf
│               ├── versions.tf
│               ├── deploy.tftest.hcl
│               └── test.sh
│
├── .github/
│   └── workflows/
│       ├── app-tests.yml                  # Tests application CI
│       ├── infra-tests.yml                # Tests infrastructure CI
│       ├── deploy-plan.yml                # Plan OpenTofu
│       ├── deploy-apply.yml               # Apply OpenTofu
│       └── deploy-destroy.yml             # Destruction ressources
│
├── kubernetes/
│   ├── deployments/
│   │   └── sample-app.yaml
│   ├── services/
│   │   └── sample-app-service.yaml
│   └── flux/
│       ├── flux-config.yaml
│       └── kustomization.yaml
│
├── docs/
│   ├── OIDC_SETUP.md                      # Configuration OIDC
│   ├── CI_CD_PIPELINE.md                  # Documentation CI/CD
│   ├── GITHUB_SECRETS.md                  # Gestion des secrets
│   ├── DEPLOYMENT_STRATEGIES.md           # Stratégies de déploiement
│   ├── GITOPS_FLUX.md                     # GitOps avec Flux
│   └── TROUBLESHOOTING.md                 # Dépannage
│
├── .gitignore
└── .env.example                           # Variables d'environnement
```

## 📊 Statistiques par Type de Fichier

| Type | Nombre | Exemples |
|------|--------|----------|
| Fichiers JavaScript | 4 | app.js, server.js, test.js |
| Fichiers Tests | 3 | *.test.js |
| Fichiers Terraform | 15+ | main.tf, variables.tf |
| Fichiers Workflow | 5 | *.yml in .github/workflows |
| Fichiers Kubernetes | 4 | *.yaml |
| Documentation | 6 | *.md in docs/ |

## 🎯 Flux de Travail

### Flux de Développement

```
Modification du code
    ↓
Push vers branche feature
    ↓
GitHub Actions déclenché
    ├── Tests d'application (Jest)
    ├── Tests d'infrastructure (OpenTofu)
    └── Analyse de couverture
    ↓
Créer Pull Request
    ↓
Review et approbation
    ↓
Merger dans main
    ↓
Déploiement automatique (CD)
    ↓
✅ Production
```

### Flux CI/CD

```
App Push
    ├── app-tests.yml
    │   ├── Install npm
    │   ├── Run npm test
    │   └── Coverage report
    │
    └── infra-tests.yml
        ├── Configure AWS credentials (OIDC)
        ├── tofu init
        └── tofu test

Pull Request
    └── deploy-plan.yml
        ├── tofu init
        ├── tofu plan
        └── Post results in PR

Merge to main
    └── deploy-apply.yml
        ├── tofu init
        ├── tofu apply
        └── Notify deployment
```

## 🔑 Fichiers Clés

### Application

| Fichier | Objectif | Chemin |
|---------|----------|--------|
| app.js | Application Express | scripts/sample-app/ |
| jest.config.js | Configuration Jest | scripts/sample-app/ |
| package.json | Dépendances NPM | scripts/sample-app/ |
| __tests__/ | Tests unitaires | scripts/sample-app/ |

### Infrastructure

| Fichier | Objectif | Chemin |
|---------|----------|--------|
| main.tf (OIDC) | Configuration OIDC | scripts/tofu/modules/github-aws-oidc/ |
| main.tf (IAM) | Rôles IAM | scripts/tofu/modules/gh-actions-iam-roles/ |
| main.tf (live) | Déploiement OIDC | scripts/tofu/live/ci-cd-permissions/ |
| main.tf (lambda) | Déploiement Lambda | scripts/tofu/live/lambda-sample/ |

### Workflows

| Fichier | Objectif | Déclencheur |
|---------|----------|------------|
| app-tests.yml | Tests app | Push |
| infra-tests.yml | Tests infra | Push |
| deploy-plan.yml | Plan deploy | PR |
| deploy-apply.yml | Apply deploy | Main |
| deploy-destroy.yml | Destroy | Manuel |

## 🚀 Navigation Rapide

| Besoin | Aller à |
|--------|---------|
| Lancer l'app | `scripts/sample-app/` → `npm start` |
| Exécuter les tests | `scripts/sample-app/` → `npm test` |
| Configurer OIDC | `scripts/tofu/live/ci-cd-permissions/` |
| Voir les workflows | `.github/workflows/` |
| Déployer Lambda | `scripts/tofu/live/lambda-sample/` |

