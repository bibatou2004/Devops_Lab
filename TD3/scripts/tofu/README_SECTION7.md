# Section 7 : Modules Terraform depuis GitHub

## 📚 Vue d'ensemble

Utilisation de modules réutilisables hébergés sur GitHub avec versioning.

## ✅ Ce qui a été fait

### Module créé
- Chemin : `TD3/scripts/tofu/modules/ec2-instance/`
- Fichiers : `main.tf`, `variables.tf`, `outputs.tf`, `user-data.sh`
- Instance déployée : i-0e5b8036a2a9f660f
- IP : 3.22.170.26:8080

### Configuration utilisant le module
- Chemin : `TD3/scripts/tofu/ec2-with-modules/`
- Utilise le module local : `../modules/ec2-instance`

## 🎯 Exercise 11 : Versioning avec Git tags

### Étape 1 : Créer un Git tag

```bash
cd /home/bibawandaogo/Devops_Lab

# Créer un tag v1.0.0
git tag v1.0.0
git push origin v1.0.0

# Vérifier
git tag -l
```

### Étape 2 : Utiliser le tag dans main.tf

```hcl
module "sample_app" {
  source = "github.com/bibatou2004/Devops_Lab.git//TD3/scripts/tofu/modules/ec2-instance?ref=v1.0.0"
  
  ami_id              = var.ami_id
  instance_count      = var.instance_count
  app_name            = "sample-app-v1"
}
```

### Étape 3 : Initialiser et déployer

```bash
terraform init
terraform plan
terraform apply
```

## 🎯 Exercise 12 : Module du Registry Terraform

### Exemple : Utiliser le module VPC du Registry

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "sample-app-vpc"
  cidr = "10.0.0.0/16"

  azs             = ["us-east-2a", "us-east-2b"]
  public_subnets = ["10.0.1.0/24", "10.0.2.0/24"]

  enable_nat_gateway = false

  tags = {
    Name = "sample-app-vpc"
  }
}
```

### Commandes

```bash
# Initialiser (télécharge le module du Registry)
terraform init

# Voir le plan
terraform plan

# Appliquer
terraform apply
```

## 📊 Résultats des déploiements

### Déploiement 1 : Single instance
```
Instance : i-0e5b8036a2a9f660f
IP       : 3.22.170.26
URL      : http://3.22.170.26:8080
Status   : ✅ Running
```

## 🔑 Concepts clés

### 1. Source locale
```hcl
source = "../modules/ec2-instance"
```

### 2. Source GitHub avec tag
```hcl
source = "github.com/user/repo.git//path/to/module?ref=v1.0.0"
```

### 3. Source Registry
```hcl
source  = "terraform-aws-modules/vpc/aws"
version = "5.0.0"
```

### 4. Avantages des modules

✅ **Réutilisabilité** : Partager entre projets
✅ **Versioning** : Contrôle des versions
✅ **Maintenance** : Mises à jour centralisées
✅ **Abstraction** : Cacher la complexité

## 📁 Structure finale

```
TD3/scripts/tofu/
├── README.md                         # Guide principal
├── README_SECTION7.md                # Ce fichier
├── MODULES_GITHUB.md                 # Exercices 11 & 12
├── modules/
│   └── ec2-instance/
│       ├── main.tf                   # Ressources
│       ├── variables.tf              # Variables
│       ├── outputs.tf                # Outputs
│       └── user-data.sh              # Script
├── ec2-instance/                     # Config simple (1 instance)
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── user-data.sh
│   └── terraform.tfvars
└── ec2-with-modules/                 # Config avec modules
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── terraform.tfvars
```

## 🧹 Nettoyage

```bash
# Détruire les instances
cd /home/bibawandaogo/devops_base/TD3/scripts/tofu/ec2-with-modules
terraform destroy -auto-approve
```

## ✅ Checklist

- [x] Module créé localement
- [x] Instance déployée via module
- [x] Application testée (3.22.170.26:8080)
- [ ] Git tag créé (v1.0.0)
- [ ] Module utilisé depuis GitHub
- [ ] Module du Registry Terraform utilisé

