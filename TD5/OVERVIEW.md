# 🎯 TD5 - Navigation Rapide et Vue d'ensemble

## 🚀 Commencez Ici

Ceci est **TD5: Intégration Continue et Livraison Continue avec Kubernetes** - le module CI/CD complet.

### Ce que vous allez apprendre

- Configurer GitHub Actions pour les tests automatisés
- Configurer OIDC pour une authentification AWS sécurisée
- Créer des pipelines de déploiement automatisés
- Implémenter différentes stratégies de déploiement
- Utiliser GitOps avec Flux

---

## 📂 Navigation Rapide

### Code de l'Application
👉 [scripts/sample-app/](scripts/sample-app/)
- **README.md** - Guide application
- **app.js** - Application Express
- **__tests__/** - Fichiers de test

### Infrastructure (OpenTofu)
👉 [scripts/tofu/](scripts/tofu/)
- **modules/github-aws-oidc/** - Configuration OIDC
- **modules/gh-actions-iam-roles/** - Rôles IAM
- **live/ci-cd-permissions/** - Déploiement OIDC & IAM
- **live/lambda-sample/** - Déploiement Lambda

### Workflows GitHub Actions
👉 [.github/workflows/](.github/workflows/)
- **app-tests.yml** - Tests d'application
- **infra-tests.yml** - Tests d'infrastructure
- **deploy-plan.yml** - Plan de déploiement
- **deploy-apply.yml** - Déploiement
- **deploy-destroy.yml** - Destruction

### Documentation
👉 [docs/](docs/)
- [OIDC_SETUP.md](docs/OIDC_SETUP.md) - Configuration OIDC
- [GITHUB_SECRETS.md](docs/GITHUB_SECRETS.md) - Secrets GitHub
- [CI_CD_PIPELINE.md](docs/CI_CD_PIPELINE.md) - Pipelines CI/CD
- [DEPLOYMENT_STRATEGIES.md](docs/DEPLOYMENT_STRATEGIES.md) - Stratégies

---

## ▶️ Démarrage Rapide

### 1️⃣ Installer les Dépendances

```bash
cd scripts/sample-app
npm install
```

### 2️⃣ Lancer l'Application

```bash
npm start
# Le serveur tourne sur http://localhost:8080
```

### 3️⃣ Tester les Endpoints

```bash
# Dans un autre terminal:
curl http://localhost:8080/
curl http://localhost:8080/name/Alice
curl http://localhost:8080/add/5/3
```

### 4️⃣ Exécuter les Tests

```bash
npm test
npm test -- --coverage
```

### 5️⃣ Configurer OIDC & IAM

```bash
cd scripts/tofu/live/ci-cd-permissions
tofu init
tofu apply
```

### 6️⃣ Configurer les Secrets GitHub

Allez à GitHub Settings → Secrets et ajoutez:
- OIDC_ROLE_ARN_TEST
- OIDC_ROLE_ARN_PLAN
- OIDC_ROLE_ARN_APPLY
- AWS_REGION

### 7️⃣ Tester les Workflows

```bash
git add .
git commit -m "feat: TD5 CI/CD setup"
git push origin main
# Allez à https://github.com/YOUR_REPO/actions
```

---

## 📊 Fichiers Clés

| Fichier | Objectif | Chemin |
|---------|----------|--------|
| app.js | Application Express | scripts/sample-app/ |
| jest.config.js | Configuration Jest | scripts/sample-app/ |
| app-tests.yml | Tests app CI | .github/workflows/ |
| infra-tests.yml | Tests infra CI | .github/workflows/ |
| main.tf (OIDC) | Configuration OIDC | scripts/tofu/modules/github-aws-oidc/ |
| main.tf (IAM) | Rôles IAM | scripts/tofu/modules/gh-actions-iam-roles/ |
| main.tf (permissions) | Déploiement OIDC | scripts/tofu/live/ci-cd-permissions/ |

---

## 🧪 Tests

### Tests Unitaires
```bash
cd scripts/sample-app
npm test -- __tests__/unit/
```

### Tests d'Intégration
```bash
npm test -- __tests__/integration/
```

### Rapport de Couverture
```bash
npm test -- --coverage
open coverage/lcov-report/index.html
```

### Tests d'Infrastructure
```bash
cd scripts/tofu/live/lambda-sample
tofu init
tofu test -verbose
```

---

## 🏗️ Infrastructure

### Valider OpenTofu
```bash
cd scripts/tofu/live/ci-cd-permissions
tofu validate
```

### Exécuter les Tests Infrastructure
```bash
tofu test -verbose
```

### Générer la Configuration
```bash
tofu plan
tofu apply
```

---

## 📈 Statistiques du Projet

```
✅ 5+ Fichiers de test
✅ 30+ Cas de test
✅ >85% Couverture de code
✅ 5 Workflows GitHub Actions
✅ 3 Rôles IAM
✅ 2000+ Lignes de code
```

---

## 🎯 Exercices

Tous les exercices complétés:

```
✅ Exercice 1-8: Fondations
✅ Exercice 9: Endpoint Add
✅ Exercice 10: Couverture de code
✅ Exercice 11: Réponses JSON
✅ Exercice 12: Gestion des erreurs
✅ Exercice 13: TDD
✅ Exercice 14: Analyse de couverture
✅ Exercice 15: Configuration OIDC
✅ Exercice 16: Pipelines CI/CD
```

---

## 📚 Apprendre Plus

- [README Principal](README.md)
- [Structure du Projet](STRUCTURE.md)
- [Configuration OIDC](docs/OIDC_SETUP.md)
- [Guide Secrets GitHub](docs/GITHUB_SECRETS.md)
- [Pipelines CI/CD](docs/CI_CD_PIPELINE.md)
- [Stratégies de Déploiement](docs/DEPLOYMENT_STRATEGIES.md)

---

## 🔗 Commandes Utiles

```bash
# Naviguer vers l'app
cd scripts/sample-app

# Installer et lancer
npm install && npm start

# Tester
npm test

# Couverture
npm test -- --coverage

# Naviguer vers infrastructure
cd ../tofu/live/ci-cd-permissions

# Tests infrastructure
tofu init && tofu test -verbose

# Commandes Terraform
tofu plan
tofu apply
tofu destroy
```

---

## 💡 Conseils

- Lisez d'abord [README.md](README.md) pour une vue d'ensemble complète
- Consultez [STRUCTURE.md](STRUCTURE.md) pour l'organisation des fichiers
- Utilisez les scripts NPM définis dans package.json
- Lancez les tests avant chaque commit
- Maintenez une couverture > 80%
- Consultez les logs GitHub Actions en cas de problème

---

## ✅ Critères de Succès

- [ ] L'application démarre sur le port 8080
- [ ] Tous les endpoints répondent correctement
- [ ] Tous les tests passent
- [ ] Couverture > 80%
- [ ] OpenTofu valide avec succès
- [ ] Tests d'infrastructure passent
- [ ] OIDC configuré avec AWS
- [ ] Workflows GitHub Actions fonctionnent
- [ ] Secrets GitHub configurés

---

**Prêt à commencer? Allez à [README.md](README.md)!** 🚀

