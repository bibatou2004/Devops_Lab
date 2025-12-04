# Guide de Troubleshooting

## Problèmes courants et solutions

### SSH Connection Timeout

**Symptôme** :
```
ssh: connect to host X.X.X.X port 22: Connection timed out
```

**Causes possibles** :
1. Instance EC2 pas encore prête
2. Security group ne permet pas SSH (port 22)
3. IP publique pas assignée

**Solutions** :
```bash
# Vérifier que l'instance est running
aws ec2 describe-instances --instance-ids <id> --region us-east-2

# Vérifier la public IP
aws ec2 describe-instances --instance-ids <id> \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --region us-east-2

# Attendre 60-90s après création
sleep 90

# Vérifier le security group
aws ec2 describe-security-groups --group-names sample-app-ansible \
  --region us-east-2
```

### Permission Denied (publickey)

**Symptôme** :
```
Permission denied (publickey,gssapi-keyex,gssapi-with-mic)
```

**Causes possibles** :
1. Clé SSH incorrecte
2. Utilisateur SSH incorrect
3. Clé n'a pas les permissions 0600

**Solutions** :
```bash
# Vérifier les permissions de la clé
ls -la ansible-ch2.key
chmod 600 ansible-ch2.key

# Vérifier le bon utilisateur
ssh -i ansible-ch2.key ec2-user@<IP> "whoami"

# Pas bibawandaogo ni root !

# Tester avec verbosité SSH
ssh -vvv -i ansible-ch2.key ec2-user@<IP>
```

### Ansible Cannot Find Host

**Symptôme** :
```
[ERROR]: Unable to parse <IP> as an inventory source
```

**Causes possibles** :
1. Inventory n'est pas dans le PATH
2. Plugin AWS EC2 non installé
3. Credentials AWS manquants

**Solutions** :
```bash
# Vérifier que ansible.cfg existe
cat ansible.cfg

# Installer le plugin AWS
ansible-galaxy collection install amazon.aws

# Configurer les credentials
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...

# Tester l'inventory
ansible-inventory -i inventory.aws_ec2.yml --graph
```

### Playbook Fails at Gathering Facts

**Symptôme** :
```
TASK [Gathering Facts] ***
fatal: [host]: UNREACHABLE
```

**Causes possibles** :
1. Python pas installé sur l'instance
2. Utilisateur sans accès
3. Firewall bloque SSH

**Solutions** :
```bash
# Se connecter manuellement et vérifier Python
ssh -i ansible-ch2.key ec2-user@<IP> "python3 --version"

# Installer Python si besoin
ssh -i ansible-ch2.key ec2-user@<IP> "sudo yum install -y python3"

# Forcer Python 3.9 dans Ansible
echo "[defaults]
interpreter_python=/usr/bin/python3.9" >> ansible.cfg
```

### YAML Syntax Error

**Symptôme** :
```
ERROR! mapping values are not allowed here
```

**Causes possibles** :
1. Indentation incorrecte
2. Caractères spéciaux mal échappés
3. Syntaxe YAML invalide

**Solutions** :
```bash
# Valider avec yamllint
yamllint *.yml

# Vérifier les indentations
cat -A playbook.yml | head -20

# Utiliser un éditeur avec support YAML
# VS Code avec extension YAML
```

### EC2 Instance Launch Fails

**Symptôme** :
```
InvalidParameterCombination: The specified instance type is not eligible
```

**Causes possibles** :
1. Instance type n'existe plus
2. Region ne supporte pas ce type
3. Limite de compte atteinte

**Solutions** :
```bash
# Lister les types disponibles
aws ec2 describe-instance-types --region us-east-2 \
  --filters "Name=free-tier-eligible,Values=true"

# Changer le type d'instance
instance_type: t3.micro  # Utiliser ce type à la place
```

### Application Ne Répond Pas sur Port 8080

**Symptôme** :
```
curl: (7) Failed to connect to X.X.X.X port 8080
```

**Causes possibles** :
1. Application pas démarrée
2. Security group ne permet pas le port 8080
3. Application crash

**Solutions** :
```bash
# Vérifier que l'app écoute
ssh -i ansible-ch2.key ec2-user@<IP> "ss -tlnp | grep 8080"

# Vérifier les logs
ssh -i ansible-ch2.key ec2-user@<IP> "tail -50 /home/ec2-user/app.log"

# Redémarrer l'app
ssh -i ansible-ch2.key ec2-user@<IP> "killall node && sleep 2 && \
  nohup node /home/ec2-user/app.js > /home/ec2-user/app.log 2>&1 &"

# Vérifier le security group
aws ec2 describe-security-groups --group-names sample-app-ansible \
  --region us-east-2
```

### Ansible Vault Password Error

**Symptôme** :
```
ERROR! The vault password client script (vault-pass.py) was not executable
```

**Solution** :
```bash
chmod +x vault-pass.py
```

### Rate Limit API AWS

**Symptôme** :
```
botocore.exceptions.ClientError: Rate Exceeded
```

**Solution** :
```bash
# Attendre et réessayer
sleep 60
ansible-playbook configure_sample_app_playbook.yml
```

## Checklist Debug

- [ ] AWS credentials configurés ?
- [ ] Instance en état "running" ?
- [ ] Public IP assignée ?
- [ ] Security group autorise port 22 et 8080 ?
- [ ] Clé SSH a les permissions 0600 ?
- [ ] Correct utilisateur SSH (ec2-user) ?
- [ ] Ansible inventory correct ?
- [ ] Python installé sur l'instance ?
- [ ] Application démarre sans erreur ?

## Support

Consulter les logs avec maximum verbosité :
```bash
ansible-playbook -vvv -i inventory.aws_ec2.yml configure_sample_app_playbook.yml
```

