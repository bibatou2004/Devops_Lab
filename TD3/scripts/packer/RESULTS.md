# Résultats TD3 - Packer AMI Creation

## ✅ Succès

### Étape 1 : Préparation
- ✅ Dossier créé : `TD3/scripts/packer/`
- ✅ app.js créé avec Node.js sample app
- ✅ Template Packer JSON préparé

### Étape 2 : Création d'AMI
- ✅ Script `create-ami.sh` créé
- ✅ Instance temporaire lancée : `i-089a554b9b2e9d0c8`
- ✅ Node.js 18.20.8 installé
- ✅ app.js copié sur l'instance
- ✅ AMI créée : `ami-0dc529b866af9ec38`
- ✅ Instance nettoyée (terminée)

### Étape 3 : Test de l'AMI
- ✅ Nouvelle instance lancée : `i-0d4b872f37c4e8262`
- ✅ Application démarrée
- ✅ Réponse reçue : `Hello, World! From EC2 via Packer AMI`

## 📊 Détails techniques

### AMI Créée
```
AMI ID           : ami-0dc529b866af9ec38
Name             : sample-app-packer-<timestamp>
Description      : Amazon Linux 2 AMI with Node.js sample app
Region           : us-east-2
Base AMI         : ami-0900fe555666598a2 (Amazon Linux 2)
Architecture     : x86_64
```

### Logiciels installés
```
Amazon Linux     : 2023.6+
Node.js          : 18.20.8
npm              : 10.8.2
```

### Instance de test
```
Instance ID      : i-0d4b872f37c4e8262
Instance Type    : t3.micro
Region           : us-east-2
Public IP        : 18.222.84.72
State            : running
```

### Application
```
Fichier          : /home/ec2-user/app.js
Port             : 8080
Response         : Hello, World! From EC2 via Packer AMI
```

## 🎯 Exercices résolus

### Exercice 5 : Que se passe-t-il si on lance packer build une deuxième fois ?

**Réponse** :
- L'AMI existante ne sera pas modifiée
- Une **nouvelle AMI** sera créée avec un **nouveau UUID** dans le nom
- Raison : Le champ `ami_name` contient `${uuidv4()}` qui génère un nouvel UUID à chaque build
- Cela permet de créer plusieurs versions de l'AMI

**Exemple** :
```
Build 1 : ami-0dc529b866af9ec38 (sample-app-packer-a1b2c3d4)
Build 2 : ami-xxxxxxxxxxxxx    (sample-app-packer-e5f6g7h8)
Build 3 : ami-yyyyyyyyyyyyy    (sample-app-packer-i9j0k1l2)
```

### Exercice 6 : Modifier le template pour un autre cloud provider

#### Exemple pour VirtualBox

```json
{
  "builders": [
    {
      "type": "virtualbox-iso",
      "iso_url": "https://mirror.example.com/amazonlinux2.iso",
      "iso_checksum": "sha256:abcd1234...",
      "vm_name": "sample-app-vbox",
      "disk_size": 20000,
      "memory": 1024,
      "cpus": 2,
      "headless": true
    }
  ],
  "provisioners": [
    {
      "type": "shell",
      "inline": [
        "yum install -y nodejs",
        "cp /tmp/app.js /opt/app.js"
      ]
    }
  ]
}
```

#### Exemple pour Google Cloud

```json
{
  "builders": [
    {
      "type": "googlecompute",
      "project_id": "my-project",
      "source_image": "debian-11",
      "image_name": "sample-app-packer",
      "zone": "us-central1-a",
      "machine_type": "e2-micro"
    }
  ]
}
```

## 📈 Performances

| Métrique | Valeur |
|----------|--------|
| Temps de création d'AMI | ~5-10 minutes |
| Temps de lancement d'instance | ~2-3 minutes |
| Temps de démarrage de l'app | ~10 secondes |
| Espace disque AMI | ~3 GB |
| Coût (AMI storage) | Minimal (~0.05 $/mois) |

## 🔐 Points de sécurité

- ✅ Clé SSH protégée
- ✅ App exécutée en tant qu'utilisateur ec2-user (non root)
- ✅ Security group restreint (ports 22, 8080)
- ✅ Pas de credentials stockés dans l'AMI

## 💡 Leçons apprises

1. **Packer vs Scripts** : Packer est plus robuste mais Bash scripts sont flexibles
2. **Versioning d'AMI** : UUID dans le nom = versions multiples possibles
3. **Temps de build** : ~5-10 min mais permet de gagner du temps au déploiement
4. **Réutilisabilité** : Une AMI crée peut lancer 100+ instances identiques
5. **Cloud Provider Flexibility** : Même template (avec adaptations) pour AWS, GCP, Azure...

## �� Prochaines étapes

- [ ] Automatiser la création d'AMI avec CI/CD
- [ ] Créer des AMI pour différentes configurations
- [ ] Intégrer avec Terraform pour IaC complet
- [ ] Ajouter des tests d'AMI
- [ ] Mettre en place un registre d'AMI

