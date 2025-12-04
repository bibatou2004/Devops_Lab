# Structure du Projet

## 📂 Organisation des fichiers

```
Devops_Lab/
├── README.md                           # Guide complet du projet
├── TROUBLESHOOTING.md                  # Guide de résolution de problèmes
├── PROJECT_STRUCTURE.md                # Ce fichier
│
├── ansible.cfg                         # Configuration Ansible globale
├── inventory.aws_ec2.yml               # Inventory dynamique AWS
│
├── create_ec2_instance_playbook.yml    # 🔨 Playbook 1 : Création EC2
├── configure_sample_app_playbook.yml   # 🚀 Playbook 2 : Configuration app
│
├── group_vars/
│   └── ch2_instances.yml               # Variables pour les instances
│
└── roles/
    └── sample-app/
        ├── tasks/
        │   └── main.yml                # Tâches d'installation Node.js
        └── files/
            └── app.js                  # Application Node.js sample
```

## 🎯 Flux de déploiement

```
┌─────────────────────────────────────────┐
│  1. create_ec2_instance_playbook.yml   │
│  - Crée security group                 │
│  - Crée clé SSH                        │
│  - Lance instance EC2                  │
└──────────────┬──────────────────────────┘
               │ Attend 90s
               ▼
┌─────────────────────────────────────────┐
│  2. configure_sample_app_playbook.yml  │
│  - Install Node.js 18                  │
│  - Copie app.js                        │
│  - Démarre l'application               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  ✅ Application accessible             │
│  http://<PUBLIC_IP>:8080               │
└─────────────────────────────────────────┘
```

## 📋 Fichiers clés

### `ansible.cfg`
Configuration globale d'Ansible :
- Chemin de la clé SSH privée
- Utilisateur SSH
- Options de connexion

### `inventory.aws_ec2.yml`
Plugin d'inventory dynamique :
- Découvre instances EC2
- Groupe par tags
- Utilise IPs publiques

### `create_ec2_instance_playbook.yml`
Crée l'infrastructure AWS :
- Security group (port 22, 8080)
- Paire de clés SSH
- Instance t3.micro
- Tags pour identification

### `configure_sample_app_playbook.yml`
Configure l'instance :
- Applique le rôle `sample-app`
- Installe Node.js
- Déploie l'application

### `roles/sample-app/tasks/main.yml`
Tâches d'installation :
- Update yum
- Setup NodeSource repo
- Install Node.js 18
- Copie application
- Démarre le service

### `roles/sample-app/files/app.js`
Application Node.js simple :
- Écoute sur port 8080
- Retourne "Hello, World! From EC2 via Ansible"

## 🔑 Variables importantes

### `group_vars/ch2_instances.yml`
```yaml
ansible_user: ec2-user                 # Utilisateur SSH
ansible_ssh_private_key_file: ...      # Chemin vers clé privée
ansible_host_key_checking: false       # Accepte nouvelles clés
ansible_ssh_common_args: ...           # Options SSH additionnelles
```

## 📊 Données de déploiement

### Instance EC2 finale
- **ID** : `i-0b1a57ea5d45cdf0c`
- **Type** : `t3.micro`
- **AMI** : Amazon Linux 2 (`ami-0900fe555666598a2`)
- **Région** : `us-east-2`
- **Public IP** : `3.143.241.36`
- **Tags** : 
  - `Name: sample-app-ansible`
  - `Ansible: ch2_instances`

### Security Group
- **Nom** : `sample-app-ansible`
- **Port 22** : SSH (0.0.0.0/0)
- **Port 8080** : HTTP (0.0.0.0/0)

### Application déployée
- **Runtime** : Node.js 18.20.8
- **Port** : 8080
- **Endpoint** : `http://3.143.241.36:8080`
- **Response** : `Hello, World! From EC2 via Ansible`

## 🔐 Fichiers sensibles (dans .gitignore)

```
ansible-ch2.key          # Clé SSH privée ⚠️
sample-ap.pem           # Clé AWS ⚠️
```

⚠️ **Ne jamais commiter les clés privées !**

## 🚀 Commandes essentielles

```bash
# Validation
yamllint *.yml
ansible-playbook --syntax-check *.yml

# Exécution
ansible-playbook -v create_ec2_instance_playbook.yml
sleep 90
ansible-playbook -v -i inventory.aws_ec2.yml configure_sample_app_playbook.yml

# Test
curl http://<PUBLIC_IP>:8080

# Nettoyage
aws ec2 terminate-instances --instance-ids <ID> --region us-east-2
```

## 📚 Documentation de référence

- [README.md](README.md) - Guide complet
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Résolution de problèmes
- [Ansible Documentation](https://docs.ansible.com/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)

## 👨‍💻 Auteur

Bibawandaogo

## 📄 Licence

MIT

