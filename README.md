# Déploiement Ansible d'une Application Node.js sur AWS EC2

## 📋 Vue d'ensemble

Ce projet automatise le déploiement d'une application Node.js sur une instance AWS EC2 en utilisant Ansible. Il inclut :
- **Création d'instance EC2** (t3.micro)
- **Configuration de security groups**
- **Gestion des clés SSH**
- **Installation de Node.js 18**
- **Déploiement d'une application sample**
- **Inventaire dynamique AWS**

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│  Ansible Control Node (Local Machine)           │
│  - create_ec2_instance_playbook.yml             │
│  - configure_sample_app_playbook.yml            │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
        ┌─────────────────────┐
        │   AWS EC2           │
        │  Instance t3.micro  │
        │  - Security Group   │
        │  - Public IP        │
        │  - Node.js 18       │
        │  - Sample App       │
        │  - Port 8080        │
        └─────────────────────┘
```

## 🚀 Démarrage rapide

### Prérequis

```bash
# Python 3.10+
python3 --version

# Ansible 2.17+
ansible --version

# AWS CLI
aws --version

# Collections Ansible
ansible-galaxy collection install amazon.aws
```

### Installation des dépendances

```bash
# Installer boto3 et botocore
pip install --user boto3 botocore

# Installer yamllint
pip install --user yamllint

# Configurer le PATH (si besoin)
export PATH="$HOME/.local/bin:$PATH"
```

### Configuration AWS

```bash
# Exporter les credentials AWS
export AWS_ACCESS_KEY_ID=votre_access_key
export AWS_SECRET_ACCESS_KEY=votre_secret_key
export AWS_DEFAULT_REGION=us-east-2

# Vérifier la connexion
aws ec2 describe-instances --region us-east-2
```

### Lancer le déploiement

```bash
# 1) Valider les fichiers YAML
yamllint *.yml group_vars/*.yml roles/*/tasks/*.yml

# 2) Vérifier la syntaxe des playbooks
ansible-playbook --syntax-check create_ec2_instance_playbook.yml
ansible-playbook --syntax-check configure_sample_app_playbook.yml

# 3) Test en dry-run (simulation)
ansible-playbook --check -v create_ec2_instance_playbook.yml

# 4) Créer l'instance EC2
ansible-playbook -v create_ec2_instance_playbook.yml

# 5) Attendre 90s que l'instance soit prête
sleep 90

# 6) Configurer l'instance
ansible-playbook -v -i inventory.aws_ec2.yml configure_sample_app_playbook.yml

# 7) Tester l'application
PUBLIC_IP=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=sample-app-ansible" "Name=instance-state-name,Values=running" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --region us-east-2 \
  --output text)

curl http://$PUBLIC_IP:8080
```

## 📁 Structure du projet

```
.
├── README.md                                    # Ce fichier
├── ansible.cfg                                  # Configuration Ansible
├── inventory.aws_ec2.yml                       # Inventory dynamique AWS
├── create_ec2_instance_playbook.yml            # Playbook création EC2
├── configure_sample_app_playbook.yml           # Playbook configuration
├── group_vars/
│   └── ch2_instances.yml                       # Variables des hosts
├── roles/
│   └── sample-app/
│       └── tasks/
│           └── main.yml                        # Tâches d'installation
└── files/
    └── app.js                                  # Application sample
```

## 🔧 Fichiers clés

### create_ec2_instance_playbook.yml
Crée une instance EC2 avec :
- Security group (port 22 et 8080)
- Paire de clés SSH
- Tags pour l'inventaire dynamique

### configure_sample_app_playbook.yml
Configure l'instance avec :
- Mise à jour yum
- Installation Node.js 18
- Copie de l'application
- Démarrage du service

### inventory.aws_ec2.yml
Plugin d'inventory dynamique qui :
- Découvre les instances EC2
- Groupe par tags
- Utilise les IPs publiques

## 🐛 Problèmes rencontrés et solutions

### 1. ❌ `yamllint` pas trouvé après installation
**Cause** : Le chemin `~/.local/bin` n'était pas dans le PATH

**Solution** :
```bash
export PATH="$HOME/.local/bin:$PATH"
# Ou installer globalement
sudo apt install yamllint
```

### 2. ❌ `security_group_ids` non reconnu
**Cause** : Le module `amazon.aws.ec2_instance` n'accepte pas ce paramètre

**Solution** : Utiliser `security_groups` à la place
```yaml
security_groups:
  - "{{ aws_security_group.group_name }}"
```

### 3. ❌ EC2 instance inaccessible (timeout)
**Cause** : Tentative de connexion à l'IP privée au lieu de l'IP publique

**Solution** : Configurer l'inventory pour utiliser les IPs publiques
```yaml
compose:
  ansible_host: public_ip_address
hostnames:
  - dns-name
```

### 4. ❌ SSH Permission denied
**Cause** : Clé privée créée après l'instance (instance créée avec ancienne clé)

**Solution** : Supprimer l'instance et la recréer avec la nouvelle clé
```bash
aws ec2 terminate-instances --instance-ids <instance-id>
ansible-playbook create_ec2_instance_playbook.yml
```

### 5. ❌ `t2.micro` plus éligible au Free Tier
**Cause** : AWS a changé les instance types Free Tier

**Solution** : Utiliser `t3.micro` ou `t2.small`
```yaml
instance_type: t3.micro
```

### 6. ❌ Paramètre `warn` non reconnu
**Cause** : Le paramètre `warn` a été supprimé dans Ansible 2.14+

**Solution** : Retirer le paramètre `warn`
```yaml
# Avant
- name: Setup NodeSource
  shell: curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
  args:
    warn: false

# Après
- name: Setup NodeSource
  shell: curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
```

### 7. ❌ Ansible ne trouve pas la clé SSH
**Cause** : SSH essayait les clés locales avant celle spécifiée

**Solution** : Ajouter `IdentitiesOnly=yes` dans `ansible.cfg`
```ini
[defaults]
ssh_args = -o IdentitiesOnly=yes
```

### 8. ❌ Host pattern `ch2_instances` ne correspond à rien
**Cause** : L'inventory dynamique crée le groupe `_ch2_instances` (avec underscore)

**Solution** : Utiliser le bon nom de groupe
```yaml
hosts: _ch2_instances  # Au lieu de ch2_instances
```

## 📊 Résultats finaux

✅ **Instance EC2 créée**
- ID : `i-0b1a57ea5d45cdf0c`
- Type : `t3.micro`
- IP Publique : `3.143.241.36`
- Région : `us-east-2`

✅ **Application déployée**
- Runtime : Node.js 18.20.8
- Port : 8080
- Response : `Hello, World! From EC2 via Ansible`

✅ **Infrastructure testée**
```bash
$ curl http://3.143.241.36:8080
Hello, World! From EC2 via Ansible
```

## 🔐 Sécurité

⚠️ **Points importants** :
- Garder les clés SSH privées en dehors du repository (`.gitignore`)
- Ne pas commiter les credentials AWS
- Utiliser des variables d'environnement pour les secrets
- Activer MFA sur le compte AWS
- Limiter les permissions du security group

## 📝 Logs et debugging

### Voir les logs détaillés
```bash
# Verbose mode
ansible-playbook -v configure_sample_app_playbook.yml

# Ultra verbose (debug)
ansible-playbook -vvv configure_sample_app_playbook.yml

# Sauvegarder les logs
ansible-playbook configure_sample_app_playbook.yml > deploy.log 2>&1
```

### Se connecter à l'instance
```bash
ssh -i ansible-ch2.key ec2-user@3.143.241.36

# Vérifier l'application
ps aux | grep node
tail -f /home/ec2-user/app.log
```

## 🧹 Nettoyage

```bash
# Terminer l'instance EC2
aws ec2 terminate-instances --instance-ids i-0b1a57ea5d45cdf0c --region us-east-2

# Supprimer la clé SSH (optionnel)
aws ec2 delete-key-pair --key-name ansible-ch2 --region us-east-2

# Supprimer le security group (après termination)
aws ec2 delete-security-group --group-name sample-app-ansible --region us-east-2
```

## 📚 Documentation complète

- [Ansible AWS Collection](https://docs.ansible.com/ansible/latest/collections/amazon/aws/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)

## 👤 Auteur

Bibawandaogo

## 📄 Licence

MIT

