#!/bin/bash

set -e

echo "🔨 Création d'une AMI avec Node.js via AWS CLI..."

# 1) Lancer une instance temporaire
echo "1️⃣  Lancer instance temporaire..."
INSTANCE_ID=$(aws ec2 run-instances \
  --image-id ami-0900fe555666598a2 \
  --instance-type t3.micro \
  --region us-east-2 \
  --key-name ansible-ch2 \
  --security-groups sample-app-ansible \
  --query 'Instances[0].InstanceId' \
  --output text)

echo "✅ Instance lancée : $INSTANCE_ID"

# 2) Attendre que l'instance soit prête
echo "2️⃣  Attendre que l'instance soit prête..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region us-east-2
sleep 30

# 3) Récupérer l'IP publique
PUBLIC_IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --region us-east-2 \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

echo "✅ IP publique : $PUBLIC_IP"

# 4) Copier app.js sur l'instance
echo "3️⃣  Copier app.js..."
scp -i /home/bibawandaogo/devops_base/td2/scripts/ansible/ansible-ch2.key \
  -o StrictHostKeyChecking=no \
  -o IdentitiesOnly=yes \
  app.js ec2-user@$PUBLIC_IP:/home/ec2-user/

echo "✅ app.js copié"

# 5) Installer Node.js sur l'instance
echo "4️⃣  Installer Node.js..."
ssh -i /home/bibawandaogo/devops_base/td2/scripts/ansible/ansible-ch2.key \
  -o StrictHostKeyChecking=no \
  -o IdentitiesOnly=yes \
  ec2-user@$PUBLIC_IP << 'SHELL'
  curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
  sudo yum install -y nodejs
  node --version
  npm --version
SHELL

echo "✅ Node.js installé"

# 6) Créer une AMI à partir de cette instance
echo "5️⃣  Créer l'AMI..."
AMI_ID=$(aws ec2 create-image \
  --instance-id $INSTANCE_ID \
  --name "sample-app-packer-$(date +%s)" \
  --description "Amazon Linux 2 AMI with Node.js sample app" \
  --region us-east-2 \
  --query 'ImageId' \
  --output text)

echo "✅ AMI créée : $AMI_ID"

# 7) Attendre que l'AMI soit prête
echo "6️⃣  Attendre que l'AMI soit disponible..."
aws ec2 wait image-available --image-ids $AMI_ID --region us-east-2

echo "✅ AMI disponible"

# 8) Terminer l'instance temporaire
echo "7️⃣  Nettoyer (terminer l'instance)..."
aws ec2 terminate-instances --instance-ids $INSTANCE_ID --region us-east-2

echo ""
echo "====== SUCCÈS ======"
echo "✅ AMI créée : $AMI_ID"
echo "📝 Utilise cette AMI pour lancer des instances avec Node.js pré-installé"
echo ""
