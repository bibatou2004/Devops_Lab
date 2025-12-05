# TD3 - Packer AMI Creation

## 📚 Vue d'ensemble

Ce projet crée une **Amazon Machine Image (AMI)** avec Node.js pré-installé en utilisant Packer.

## 🎯 Objectifs

✅ Créer une AMI personnalisée avec Node.js 18
✅ Automatiser le processus d'image building
✅ Réutiliser l'AMI pour lancer rapidement des instances

## 📁 Structure

```
TD3/scripts/packer/
├── README.md                    # Ce fichier
├── app.js                       # Application Node.js
├── sample-app.json              # Template Packer (JSON)
├── create-ami.sh                # Script de création d'AMI
└── RESULTS.md                   # Résultats finaux
```

## 🚀 Déploiement

### Prérequis

```bash
# Packer 1.9+
packer version

# AWS CLI configuré
aws configure

# Clé SSH disponible
ls ~/.ssh/ansible-ch2.key
```

### Méthode 1 : Via script Bash (Recommandé)

```bash
cd TD3/scripts/packer

# Rendre le script exécutable
chmod +x create-ami.sh

# Lancer la création d'AMI
./create-ami.sh

# Récupère l'AMI ID à la fin
```

### Méthode 2 : Via Packer JSON

```bash
cd TD3/scripts/packer

# Valider le template
packer validate sample-app.json

# Construire l'AMI
packer build sample-app.json
```

## 📊 Résultats

### AMI Créée
- **AMI ID** : `ami-0dc529b866af9ec38`
- **Description** : Amazon Linux 2 AMI with Node.js sample app
- **Node.js Version** : 18.20.8
- **npm Version** : 10.8.2

### Instance de Test
- **Instance ID** : `i-0d4b872f37c4e8262`
- **Instance Type** : t3.micro
- **Public IP** : 18.222.84.72
- **Application Response** : `Hello, World! From EC2 via Packer AMI`

## 🧪 Tests

### Tester l'application

```bash
# Via curl
curl http://18.222.84.72:8080

# Via SSH
ssh -i ~/.ssh/ansible-ch2.key ec2-user@18.222.84.72
node /home/ec2-user/app.js
```

### Vérifier Node.js

```bash
ssh -i ~/.ssh/ansible-ch2.key ec2-user@18.222.84.72
node --version
npm --version
```

## 🔄 Réutiliser l'AMI

```bash
# Lancer une nouvelle instance avec cette AMI
aws ec2 run-instances \
  --image-id ami-0dc529b866af9ec38 \
  --instance-type t3.micro \
  --region us-east-2 \
  --key-name ansible-ch2 \
  --security-groups sample-app-ansible
```

## 📝 Template Packer (JSON)

```json
{
  "builders": [
    {
      "type": "amazon-ebs",
      "ami_name": "sample-app-packer-{{timestamp}}",
      "ami_description": "Amazon Linux 2 AMI with a Node.js sample app.",
      "instance_type": "t3.micro",
      "region": "us-east-2",
      "source_ami": "ami-0900fe555666598a2",
      "ssh_username": "ec2-user"
    }
  ],
  "provisioners": [
    {
      "type": "file",
      "source": "app.js",
      "destination": "/home/ec2-user/app.js"
    },
    {
      "type": "shell",
      "inline": [
        "curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -",
        "sudo yum install -y nodejs"
      ],
      "pause_before": "30s"
    }
  ]
}
```

## 🧹 Nettoyage

### Terminer l'instance de test

```bash
aws ec2 terminate-instances \
  --instance-ids i-0d4b872f37c4e8262 \
  --region us-east-2
```

### Déregistrer l'AMI (optionnel)

```bash
aws ec2 deregister-image \
  --image-id ami-0dc529b866af9ec38 \
  --region us-east-2
```

## ✅ Points clés

- **Packer JSON** : Compatible avec versions anciennes de Packer
- **Bash Script** : Alternative à Packer, utilise AWS CLI directement
- **AMI Réutilisable** : Lancer plusieurs instances avec la même config
- **Temps de déploiement** : ~5-10 minutes pour créer une AMI
- **Avantages** : Instances prêtes immédiatement, pas d'attente de provisioning

## 🐛 Troubleshooting

### Packer ne reconnaît pas HCL
→ Utilise le format JSON à la place

### Erreur "listen: operation not permitted"
→ Nettoie le cache Packer : `rm -rf ~/.packer.d/`

### Instance type not eligible for Free Tier
→ Utilise `t3.micro` au lieu de `t2.micro`

## 📚 Documentation complète

Voir [RESULTS.md](RESULTS.md) pour les résultats détaillés.

## 👨‍💻 Auteur

Bibawandaogo

## 📄 Licence

MIT

