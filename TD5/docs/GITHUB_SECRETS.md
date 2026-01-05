# 🔑 Gestion des Secrets GitHub

## Vue d'ensemble

Les secrets GitHub stockent les informations sensibles utilisées par les workflows GitHub Actions.

## Secrets Requis pour TD5

### 1. OIDC_ROLE_ARN_TEST

**Description**: ARN du rôle IAM pour les tests d'infrastructure

**Où le trouver**:
```bash
cd scripts/tofu/live/ci-cd-permissions
tofu output lambda_test_role_arn
```

**Valeur**: `arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-sample-test-role`

**Utilisé par**: `.github/workflows/infra-tests.yml`

### 2. OIDC_ROLE_ARN_PLAN

**Description**: ARN du rôle IAM pour le plan OpenTofu

**Où le trouver**:
```bash
cd scripts/tofu/live/ci-cd-permissions
tofu output lambda_deploy_plan_role_arn
```

**Valeur**: `arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-sample-plan-role`

**Utilisé par**: `.github/workflows/deploy-plan.yml`

### 3. OIDC_ROLE_ARN_APPLY

**Description**: ARN du rôle IAM pour l'apply OpenTofu

**Où le trouver**:
```bash
cd scripts/tofu/live/ci-cd-permissions
tofu output lambda_deploy_apply_role_arn
```

**Valeur**: `arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-sample-apply-role`

**Utilisé par**: `.github/workflows/deploy-apply.yml`

### 4. AWS_REGION

**Description**: Région AWS

**Valeur**: `us-east-2` (ou votre région préférée)

**Utilisé par**: Tous les workflows AWS

---

## Comment Ajouter les Secrets

### Méthode 1: Via l'Interface Web GitHub

1. Allez à votre dépôt
2. Cliquez sur **Settings**
3. Dans la barre gauche, cliquez sur **Secrets and variables** → **Actions**
4. Cliquez sur **New repository secret**
5. Entrez:
   - **Name**: `OIDC_ROLE_ARN_TEST`
   - **Secret**: `arn:aws:iam::...`
6. Cliquez sur **Add secret**
7. Répétez pour les autres secrets

### Méthode 2: Via le CLI GitHub

```bash
# Installer GitHub CLI si nécessaire
# https://cli.github.com/

# Se connecter à GitHub
gh auth login

# Ajouter les secrets
gh secret set OIDC_ROLE_ARN_TEST --body "arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-sample-test-role"
gh secret set OIDC_ROLE_ARN_PLAN --body "arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-sample-plan-role"
gh secret set OIDC_ROLE_ARN_APPLY --body "arn:aws:iam::YOUR_ACCOUNT_ID:role/lambda-sample-apply-role"
gh secret set AWS_REGION --body "us-east-2"
```

---

## Vérifier les Secrets

```bash
# Lister les secrets existants (sans afficher les valeurs)
gh secret list
```

---

## Utiliser les Secrets dans les Workflows

Les secrets sont utilisés avec la syntaxe `${{ secrets.SECRET_NAME }}`:

```yaml
# Exemple dans un workflow
- uses: aws-actions/configure-aws-credentials@v3
  with:
    role-to-assume: ${{ secrets.OIDC_ROLE_ARN_TEST }}
    aws-region: ${{ secrets.AWS_REGION }}
```

---

## Bonnes Pratiques

✅ **À FAIRE**:
- Utiliser des rôles IAM avec permissions minimales
- Documenter tous les secrets
- Utiliser des noms clairs et descriptifs
- Mettre à jour les secrets quand les rôles IAM changent
- Auditer régulièrement l'accès aux secrets

❌ **À NE PAS FAIRE**:
- Committer les secrets dans le dépôt
- Utiliser les mêmes secrets pour tous les workflows
- Donner trop de permissions aux rôles IAM
- Oublier de mettre à jour les secrets après rotation

---

## Dépannage

### Erreur: "Secret not found"

Vérifiez:
- Le nom du secret est correct
- Le secret est ajouté au bon dépôt
- Le workflow utilise la bonne syntaxe `${{ secrets.NAME }}`

### Erreur: "Access Denied" dans les workflows

Vérifiez:
- Le rôle IAM a les bonnes permissions
- La confiance OIDC est correctement configurée
- Le repo GitHub correspond au `github_repo` dans la configuration IAM

### Les Secrets ne Sont pas Disponibles dans les Pull Requests de Fork

C'est normal ! GitHub ne passe les secrets que pour les workflows des dépôts officiels, pas des forks. Les contributeurs doivent créer leurs propres secrets.

