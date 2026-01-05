#!/usr/bin/env bash
set -e

# Région AWS

export AWS_DEFAULT_REGION="us-east-2"

# Nom de la KeyPair

KEY_NAME="sample-ap-key"

# Nom du Security Group

SG_NAME="sample-app"

# Vérifier ou créer le Security Group

existing_sg=$(aws ec2 describe-security-groups --group-names "$SG_NAME" --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null || echo "")
if [ -z "$existing_sg" ]; then
security_group_id=$(aws ec2 create-security-group 
--group-name "$SG_NAME" 
--description "Allow HTTP and SSH traffic" 
--output text 
--query GroupId)
aws ec2 authorize-security-group-ingress --group-id "$security_group_id" --protocol tcp --port 80 --cidr "0.0.0.0/0"
aws ec2 authorize-security-group-ingress --group-id "$security_group_id" --protocol tcp --port 22 --cidr "0.0.0.0/0"
echo "Security Group créé : $security_group_id"
else
security_group_id=$existing_sg
echo "Security Group déjà existant : $security_group_id"
fi

# User-data pour installer Apache

read -r -d '' USER_DATA <<'EOF'
#!/bin/bash
yum update -y
yum install -y httpd
systemctl enable httpd
systemctl start httpd
echo "Instance EC2 déployée avec succès" > /var/www/html/index.html
EOF

# Lancer l'instance EC2

INSTANCE_ID=$(aws ec2 run-instances 
--image-id "ami-025ca978d4c1d9825" 
--instance-type "t3.micro" 
--key-name "$KEY_NAME" 
--security-group-ids "$security_group_id" 
--user-data "$USER_DATA" 
--count 1 
--query 'Instances[0].InstanceId' 
--output text)

echo "Instance lancée : $INSTANCE_ID"

# Attendre que l'instance soit running

aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"

# Récupérer l'IP publique

PUBLIC_IP=$(aws ec2 describe-instances 
--instance-ids "$INSTANCE_ID" 
--query 'Reservations[0].Instances[0].PublicIpAddress' 
--output text)

echo "IP publique : $PUBLIC_IP"
echo "Pour vous connecter en SSH :"
echo "ssh -i $HOME/$KEY_NAME.pem ec2-user@$PUBLIC_IP"
