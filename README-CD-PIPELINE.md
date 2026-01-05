# 🚀 Continuous Delivery Pipeline avec Terraform

> **Part 2 de TD5:** Infrastructure as Code avec CI/CD automatisé

## 📚 Documentation Complète

Voir le [README détaillé pour TD5 Part 2](TD5/README-PART2.md)

## ⚡ Quick Start

```bash
# 1. Initialiser le backend
cd TD5/scripts/tofu/live/tofu-state
terraform init
terraform apply

# 2. Créer les rôles IAM
cd ../ci-cd-permissions
terraform init
terraform apply

# 3. Faire un changement et créer une PR
git checkout -b feature/update
# ... modifier le code ...
git commit -m "feat: Update infrastructure"
git push origin feature/update
gh pr create

# 4. Merger la PR
gh pr merge <PR_NUMBER> --auto --squash

# 5. L'infrastructure est automatiquement mise à jour! ✅
```

## 🎯 Fonctionnalités

- ✅ Infrastructure Backend (S3 + DynamoDB)
- ✅ Remote State Management
- ✅ State Locking (prévient les conflits)
- ✅ Automatic Plans on PRs
- ✅ Automatic Apply on Merge
- ✅ Secure OIDC Authentication
- ✅ GitOps Workflow
- ✅ Production Ready

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [README Complet](TD5/README-PART2.md) | Documentation exhaustive |
| [Architecture](TD5/README-PART2.md#-architecture) | Diagrammes et flux |
| [Installation](TD5/README-PART2.md#-installation) | Guide étape par étape |
| [Workflows](TD5/README-PART2.md#-workflows) | Détails des GitHub Actions |
| [Sécurité](TD5/README-PART2.md#-sécurité) | Best practices OIDC + IAM |
| [Dépannage](TD5/README-PART2.md#-dépannage) | Solutions aux problèmes |

## 🏗️ Architecture Résumée

```
GitHub PR/Merge
      ↓
GitHub Actions (OIDC)
      ↓
AWS IAM Role (Least Privilege)
      ↓
Terraform Plan/Apply
      ↓
AWS S3 Backend + DynamoDB Locking
      ↓
Infrastructure Déployée ✅
```

## 📊 Statut

| Component | Status |
|-----------|--------|
| Backend (S3 + DynamoDB) | ✅ Deployed |
| Workflows (Plan + Apply) | ✅ Configured |
| OIDC Authentication | ✅ Active |
| IAM Roles | ✅ Configured |
| Git Integration | ✅ Ready |

## 🚀 Pour démarrer

1. **Lire la documentation:** [README Complet](TD5/README-PART2.md)
2. **Installer:** Suivre la section [Installation](TD5/README-PART2.md#-installation)
3. **Tester:** Créer une PR test
4. **Déployer:** Merger et observer les workflows

## 📝 Fichiers clés

```
TD5/
├── README-PART2.md                    ← Documentation complète
├── scripts/tofu/
│   ├── modules/state-bucket/          ← Module S3 + DynamoDB
│   └── live/
│       ├── tofu-state/                ← Configuration backend
│       └── ci-cd-permissions/         ← Rôles IAM
└── .github/workflows/
    ├── tofu-plan.yml                  ← PR workflow
    └── tofu-apply.yml                 ← Main workflow
```

## 🔗 Liens utiles

- [GitHub Repository](https://github.com/bibatou2004/Devops_Lab)
- [Pull Request #1](https://github.com/bibatou2004/Devops_Lab/pull/1)
- [GitHub Actions](https://github.com/bibatou2004/Devops_Lab/actions)
- [AWS Console](https://console.aws.amazon.com)

## 🎓 Ce que tu vas apprendre

✅ Terraform Remote State Management  
✅ AWS S3 Backend Configuration  
✅ DynamoDB State Locking  
✅ GitHub Actions CI/CD  
✅ OIDC Token Authentication  
✅ IAM Roles et Policies  
✅ GitOps Workflow  
✅ Infrastructure as Code Best Practices  

## 📞 Support

Voir la section [Support](TD5/README-PART2.md#-support) du README complet

---

**Status:** ✅ Production Ready  
**Last Updated:** 2025-12-05  
**Maintained by:** [@bibatou2004](https://github.com/bibatou2004)
