# 🔐 Guide Complet de Configuration OIDC

## 📋 Checklist de Configuration

### Phase 1: Préparation AWS

- [ ] Accès AWS CLI configuré
- [ ] Permissions pour créer IAM roles et OIDC providers
- [ ] Région AWS définie (us-east-2)

### Phase 2: Déploiement Infrastructure

- [ ] Cloner le dépôt
- [ ] Naviguer à `TD5/scripts/tofu/live/ci-cd-permissions`
- [ ] Exécuter `tofu init`
- [ ] Exécuter `tofu plan` et vérifier
- [ ] Exécuter `tofu apply`
- [ ] Copier les outputs ARNs

### Phase 3: Configuration GitHub

- [ ] Aller à Settings → Secrets and variables → Actions
- [ ] Créer 4 secrets GitHub
- [ ] Tester les workflows

---

## 🚀 Déploiement Complet (Étapes Détaillées)

### Étape 1: Préparer l'Environnement AWS

```bash
# Vérifier AWS CLI
aws sts get-caller-identity

# Résultat attendu:
# {
#     "UserId": "...",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/..."
# }

# Copier votre AWS Account ID (123456789012)
```

### Étape 2: Initialiser OpenTofu

```bash
cd ~/TD4/devops-lab/TD5/scripts/tofu/live/ci-cd-permissions

# Initialiser
tofu init

# Sorties attendues:
# Downloading modules...
# Initializing the backend...
# Initializing provider plugins...
# Terraform has been successfully initialized!
```

### Étape 3: Générer le Plan

```bash
# Générer et afficher le plan
tofu plan

# Vérifier que vous voyez:
# - aws_iam_openid_connect_provider will be created
# - aws_iam_role will be created (x3)
# - aws_iam_role_policy will be created (x3)
```

### Étape 4: Appliquer la Configuration

```bash
# Appliquer (créer les ressources)
tofu apply

# Vous verrez un prompt:
# Do you want to perform these actions?
#
# Répondre: yes

# Attendez que le processus se termine
```

### Étape 5: Récupérer les Outputs

```bash
# Afficher tous les outputs
tofu output

# Résultat attendu:
# lambda_deploy_apply_role_arn = "arn:aws:iam::123456789012:role/lambda-sample-apply"
# lambda_deploy_plan_role_arn = "arn:aws:iam::123456789012:role/lambda-sample-plan"
# lambda_test_role_arn = "arn:aws:iam::123456789012:role/lambda-sample-tests"
# oidc_provider_arn = "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"

# Copier les 3 ARNs de rôle (test, plan, apply)
```

---

## 🔑 Configuration des Secrets GitHub

### Méthode 1: Via Interface Web (Recommandée)

1. **Ouvrir GitHub**
   - Aller à: https://github.com/bibatou2004/Devops_Lab/settings/secrets/actions

2. **Créer Secret 1: OIDC_ROLE_ARN_TEST**
   - Cliquer "New repository secret"
   - Name: `OIDC_ROLE_ARN_TEST`
   - Value: `arn:aws:iam::123456789012:role/lambda-sample-tests`
   - Cliquer "Add secret"

3. **Créer Secret 2: OIDC_ROLE_ARN_PLAN**
   - Name: `OIDC_ROLE_ARN_PLAN`
   - Value: `arn:aws:iam::123456789012:role/lambda-sample-plan`

4. **Créer Secret 3: OIDC_ROLE_ARN_APPLY**
   - Name: `OIDC_ROLE_ARN_APPLY`
   - Value: `arn:aws:iam::123456789012:role/lambda-sample-apply`

5. **Créer Secret 4: AWS_REGION**
   - Name: `AWS_REGION`
   - Value: `us-east-2`

### Méthode 2: Via GitHub CLI

```bash
# Se connecter à GitHub
gh auth login

# Créer les secrets
gh secret set OIDC_ROLE_ARN_TEST \
  --body "arn:aws:iam::123456789012:role/lambda-sample-tests" \
  --repo bibatou2004/Devops_Lab

gh secret set OIDC_ROLE_ARN_PLAN \
  --body "arn:aws:iam::123456789012:role/lambda-sample-plan" \
  --repo bibatou2004/Devops_Lab

gh secret set OIDC_ROLE_ARN_APPLY \
  --body "arn:aws:iam::123456789012:role/lambda-sample-apply" \
  --repo bibatou2004/Devops_Lab

gh secret set AWS_REGION \
  --body "us-east-2" \
  --repo bibatou2004/Devops_Lab
```

---

## ✅ Tests et Vérification

### Vérifier OIDC dans AWS

```bash
# Lister les providers OIDC
aws iam list-open-id-connect-providers

# Afficher les détails du provider
aws iam get-open-id-connect-provider \
  --open-id-connect-provider-arn "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com"
```

### Vérifier les Rôles IAM

```bash
# Lister les rôles
aws iam list-roles --query 'Roles[?contains(RoleName, `lambda-sample`)]'

# Afficher les politiques d'un rôle
aws iam list-role-policies --role-name lambda-sample-tests

# Afficher la relation de confiance
aws iam get-role --role-name lambda-sample-tests
```

### Tester les Workflows GitHub

1. **Créer une branche**
   ```bash
   git checkout -b test-ci
   ```

2. **Faire une petite modification**
   ```bash
   echo "# Test" >> README.md
   ```

3. **Committer et Pousser**
   ```bash
   git add .
   git commit -m "test: Test CI/CD workflows"
   git push origin test-ci
   ```

4. **Créer une Pull Request**
   - Aller à https://github.com/bibatou2004/Devops_Lab/pulls
   - Cliquer "New pull request"
   - Sélectionner `test-ci` → `main`
   - Cliquer "Create pull request"

5. **Vérifier les Workflows**
   - Aller à l'onglet "Actions"
   - Observer les workflows en cours d'exécution
   - Cliquer sur un workflow pour voir les logs

---

## 🐛 Dépannage

### Erreur: "InvalidParameterException: Invalid length for parameter ThumbprintList"

**Solution**: Utiliser le thumbprint correct dans `github-aws-oidc/main.tf`:
```
thumbprint_list = ["6938fd4d98bab03faadb97b34396831e3780aea1"]
```

### Erreur: "AccessDenied: User is not authorized to perform: iam:CreateOpenIDConnectProvider"

**Solution**: L'utilisateur AWS a besoin des permissions:
```
iam:CreateOpenIDConnectProvider
iam:CreateRole
iam:PutRolePolicy
```

### Erreur dans Workflow: "AccessDenied when assuming role"

**Vérifier**:
1. Les secrets GitHub sont correctement configurés
2. Le `github_repo` dans Terraform correspond au format `owner/repo`
3. La relation de confiance OIDC permet les branches correctes

### Workflow Pending ou Très Lent

Cela peut prendre quelques minutes. Attendez 5-10 minutes avant de conclure qu'il y a une erreur.

---

## 📝 Notes Importantes

1. **Credentials de Courte Durée**: OIDC génère des tokens valides 15 minutes
2. **Région AWS**: Assurez-vous que la région correspond partout
3. **GitHub Repo**: Format exact: `owner/repo` (pas d'URL)
4. **Permissions Minimales**: Les rôles IAM ont des permissions minimales nécessaires
5. **Audit**: Vérifiez les logs CloudTrail pour les actions AWS

---

## 🔗 Références

- [GitHub OIDC Documentation](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [AWS IAM OIDC Provider](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect#updating-your-actions-for-oidc)
- [OpenTofu Documentation](https://opentofu.org/docs/)

