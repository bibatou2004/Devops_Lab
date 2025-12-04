# TD3 Section 5 - Terraform (OpenTofu)

## 📚 Vue d'ensemble

Déploiement et gestion d'instances EC2 avec Terraform en utilisant l'AMI créée par Packer.

## 🎯 Objectifs

✅ Déployer 1 instance EC2 avec Terraform
✅ Mettre à jour la configuration en place
✅ Déployer plusieurs instances avec `count`
✅ Tester les applications

## 📁 Structure

```
TD3/scripts/tofu/
├── README.md                    # Ce fichier
├── EXERCISES.md                 # Solutions des exercices
├── ec2-instance/
│   ├── main.tf                  # Configuration AWS
│   ├── variables.tf             # Variables d'entrée
│   ├── outputs.tf               # Outputs
│   ├── terraform.tfvars         # Valeurs des variables
│   ├── user-data.sh             # Script de démarrage
│   ├── .terraform/              # Dossier Terraform (généré)
│   ├── terraform.tfstate        # État (généré)
│   └── .terraform.lock.hcl      # Lock file (généré)
```

## 🚀 Déploiement

### Prérequis

```bash
terraform version  # >= 1.0
aws configure      # AWS credentials configurés
```

### Étape 1 : Initialiser

```bash
cd ec2-instance
terraform init
```

### Étape 2 : Voir le plan

```bash
terraform plan
```

### Étape 3 : Appliquer

```bash
terraform apply
# Tape 'yes' pour confirmer
```

### Étape 4 : Voir les outputs

```bash
terraform output
```

## 📊 Déploiements effectués

### Configuration 1 : 1 Instance

```
Instance ID : i-06615cb8fd405455a
Public IP   : 18.222.147.170
Application : http://18.222.147.170:8080
```

### Configuration 2 : 1 Instance avec Tag Update

```
Changement : Ajout du tag "Test = update"
Terraform : Update in-place (aucune recréation)
```

### Configuration 3 : 3 Instances avec count

```
Instance 1 : i-0089ce8d07a32f713 (3.16.164.96)
Instance 2 : i-0d2db3f6f8152f164 (18.117.114.28)
Instance 3 : i-06629fca3cbf3a255 (18.118.131.184)

Security Group : sg-02690177838f8ced9
```

## 🧪 Tests

### Tester les 3 applications

```bash
curl http://3.16.164.96:8080
curl http://18.117.114.28:8080
curl http://18.118.131.184:8080

# Réponse attendue :
# Hello, World! From EC2 via Packer AMI
```

## 🔄 Commandes courantes

### Plan sans appliquer

```bash
terraform plan
```

### Appliquer sans confirmation

```bash
terraform apply -auto-approve
```

### Détruire les ressources

```bash
terraform destroy
# ou
terraform destroy -auto-approve
```

### Voir l'état actuel

```bash
terraform state list
terraform state show aws_instance.sample_app[0]
```

### Rafraîchir l'état

```bash
terraform refresh
```

## 📈 Concepts clés

### 1. count

Permet de créer plusieurs instances identiques :

```hcl
count = var.instance_count

# Dans les ressources :
tags = {
  Name = "instance-${count.index + 1}"
}

# Dans les outputs :
value = aws_instance.sample_app[*].id
```

### 2. State Management

- **terraform.tfstate** : Stocke l'état des ressources
- **terraform.tfstate.backup** : Backup automatique
- Doit être synchronisé avec AWS

### 3. Idempotence

- Terraform est idempotent : `apply` 2x = même résultat
- Seules les différences sont appliquées

### 4. Plan vs Apply

- **Plan** : Affiche les changements (dry-run)
- **Apply** : Exécute les changements réels

## 🧹 Cleanup

### Détruire tout

```bash
terraform destroy -auto-approve
```

### Garder les instances mais reset Terraform

```bash
rm -rf .terraform terraform.tfstate*
```

## 📝 Exercices

### Exercise 7 : terraform apply après destroy

**Réponse** : Les ressources sont recréées

```bash
terraform destroy -auto-approve
terraform apply -auto-approve
# Nouvelles IPs publiques!
```

### Exercise 8 : Déployer plusieurs instances

**Implémenté avec `count`** :

- Modifier `variable "instance_count"` dans `variables.tf`
- Modifier `instance_count = 3` dans `terraform.tfvars`
- Ajouter `count = var.instance_count` dans `main.tf`
- Ajouter `count.index` dans les tags pour noms uniques

**Résultat** : 3 instances déployées en parallèle

## 🐛 Troubleshooting

### Erreur "Reference to count in non-counted context"

→ `count` doit être dans la ressource qui l'utilise, pas dans une autre

### Erreur "State lock timeout"

→ Une autre commande Terraform est en cours, attendre

### Instances ne répondent pas

→ Attendre 30-60s pour que user-data s'exécute

```bash
aws ec2 describe-instances --instance-ids i-xxx --query 'Reservations[0].Instances[0].State'
```

## 📚 Documentation

- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform count](https://www.terraform.io/language/meta-arguments/count)
- [Terraform state](https://www.terraform.io/language/state)

## 👨‍💻 Résumé

✅ Infrastructure as Code avec Terraform
✅ Gestion d'état automatique
✅ Déploiement d'instances scalables
✅ Configuration réutilisable et versionnable

