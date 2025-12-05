# 🎓 TD5 - Intégration Continue (CI) et Livraison Continue (CD) avec Kubernetes

## 📚 Vue d'ensemble

**TD5** est un module complet de DevOps couvrant :

- ✅ **Intégration Continue (CI)** avec GitHub Actions
- ✅ **Tests Automatisés** (Application et Infrastructure)
- ✅ **Authentification OIDC** avec AWS
- ✅ **Livraison Continue (CD)** avec OpenTofu
- ✅ **Stratégies de Déploiement** (Blue/Green, Canary, etc.)
- ✅ **GitOps avec Flux**

## 🎯 Objectifs

1. Configurer CI avec tests automatisés
2. Configurer OIDC pour l'authentification AWS
3. Créer un pipeline de déploiement automatisé
4. Implémenter différentes stratégies de déploiement
5. Explorer GitOps avec Flux

## 📋 Prérequis

```bash
✅ GitHub account
✅ AWS account
✅ Local Kubernetes cluster (Docker Desktop ou Minikube)
✅ Git, Docker, kubectl, OpenTofu, npm, Node.js
✅ aws-cli, flux
```

## 🏗️ Structure du Projet

```
TD5/
├── scripts/
│   ├── sample-app/              # Application Node.js
│   └── tofu/                    # Infrastructure OpenTofu
├── .github/workflows/           # GitHub Actions pipelines
├── kubernetes/                  # Manifestes Kubernetes
└── docs/                        # Documentation
```

## 🚀 Sections

### Section 1: Intégration Continue (CI)
- Principes de CI
- Trunk-based development
- Tests automatisés avec Jest
- GitHub Actions workflows

### Section 2: Authentification OIDC avec AWS
- Configuration du fournisseur OIDC
- Création des rôles IAM
- Authentification sécurisée

### Section 3: Tests d'Infrastructure
- Tests OpenTofu
- Validation de la configuration
- Tests d'intégration

### Section 4: Livraison Continue (CD)
- Pipelines de déploiement
- Déploiement avec OpenTofu
- Stratégies de déploiement

### Section 5: GitOps avec Flux
- Configuration Flux
- Synchronisation déclarative
- Déploiement automatisé

## 📖 Documentation

- [README.md](README.md) - Guide principal (ce fichier)
- [STRUCTURE.md](STRUCTURE.md) - Structure du projet
- [OVERVIEW.md](OVERVIEW.md) - Navigation rapide
- [docs/CI_CD_PIPELINE.md](docs/CI_CD_PIPELINE.md) - Documentation CI/CD
- [docs/OIDC_SETUP.md](docs/OIDC_SETUP.md) - Configuration OIDC
- [docs/GITHUB_SECRETS.md](docs/GITHUB_SECRETS.md) - Gestion des secrets

## ⚡ Démarrage Rapide

```bash
# 1. Naviguer vers TD5
cd TD5/scripts/sample-app

# 2. Installer les dépendances
npm install

# 3. Lancer les tests
npm test

# 4. Démarrer l'application
npm start
```

## 🧪 Tests

### Tests d'Application

```bash
cd TD5/scripts/sample-app
npm install
npm test                    # Tests unitaires
npm test -- --coverage     # Rapport de couverture
```

### Tests d'Infrastructure

```bash
cd TD5/scripts/tofu/live/lambda-sample
tofu init
tofu test -verbose
```

## 📊 Workflows GitHub Actions

| Workflow | Fichier | Déclencheur |
|----------|---------|------------|
| App Tests | `app-tests.yml` | Push sur toute branche |
| Infra Tests | `infra-tests.yml` | Push sur toute branche |
| Deploy Plan | `deploy-plan.yml` | Pull request |
| Deploy Apply | `deploy-apply.yml` | Push sur main |
| Deploy Destroy | `deploy-destroy.yml` | Mannuel |

## 🔐 Secrets GitHub

À configurer dans GitHub Settings → Secrets:

```
OIDC_ROLE_ARN_TEST
OIDC_ROLE_ARN_PLAN
OIDC_ROLE_ARN_APPLY
AWS_REGION
```

## 📈 Statistiques

- **Test Files**: 5+
- **Test Cases**: 30+
- **Code Coverage**: >85%
- **Workflows**: 5
- **IAM Roles**: 3

## 🤝 Contribution

1. Créer une branche (`git checkout -b feature/amazing-feature`)
2. Faire vos modifications
3. Tester (`npm test`)
4. Committer (`git commit -m 'Add feature'`)
5. Pousser (`git push origin feature/amazing-feature`)
6. Créer une Pull Request

## 📞 Support

Pour des questions ou des problèmes:
1. Consulter la documentation
2. Vérifier les logs GitHub Actions
3. Consulter le troubleshooting

## 👤 Auteur

**Biba Wandaogo**
- GitHub: [@bibatou2004](https://github.com/bibatou2004)

## ✅ Statut

**Status**: 🚧 En construction
**Dernière mise à jour**: Décembre 5, 2025

