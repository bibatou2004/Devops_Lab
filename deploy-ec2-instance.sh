#!/usr/bin/env bash
set -e

# Nombre d'instances à lancer

NUM_INSTANCES=2

# Région AWS

export AWS_DEFAULT_REGION="us-east-2"

# Contenu du script user-data intégré

read -r -d '' user_data <<'EOF'
#!/bin/bash
yum update -y
yum install -y httpd
systemctl enable httpd
systemctl start httpd
echo "Instance EC2 déployée avec succès" > /var/www/html/index.html
EOF

# Nom de la KeyPair à utiliser

KEY_NAME="sample-ap-key"

# Créer la KeyPair si elle n'existe pas

if ! aws ec2 describe-key-pairs --key-names "$KEY_NAME" >/dev/null 2>&1; then
echo "Création de la KeyPair $KEY_NAME..."
aws ec2 create-key-pair --key-name "$KEY_NAME" --query 'KeyMaterial' --output text > "$HOME/$KEY_NAME.pem"
chmod 400 "$HOME/$KEY_NAME.pem"
echo "KeyPair créée et sauvegardée dans $HOME/$KEY_NAME.pem"
else
echo "KeyPair $KEY_NAME déjà existante."
fi

# Vérifier ou créer le Security Group

existing_sg=$(aws ec2 describe-security-groups --group-names "sample-app" --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null || echo "")
if [ -z "$existing_sg" ]; then
security_group_id=$(aws ec2 create-security-group 
--group-name "sample-app" 
--description "Allow HTTP traffic into the sample app" 
--output text 
--query GroupId)
aws ec2 authorize-security-group-ingress 
--group-id "$security_group_id" 
--protocol tcp 
--port 80 
--cidr "0.0.0.0/0" > /dev/null
echo "Security Group créé : $security_group_id"
else
security_group_id=$existing_sg
echo "Security Group déjà existant : $security_group_id"
fi

# Lancer les instances EC2

instance_ids=$(aws ec2 run-instances 
--image-id "ami-025ca978d4c1d9825" 
--instance-type "t3.micro" 
--key-name "$KEY_NAME" 
--security-group-ids "$security_group_id" 
--user-data "$user_data" 
--tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=sample-app}]' 
--count $NUM_INSTANCES 
--output text 
--query 'Instances[*].InstanceId')

# Attendre que toutes les instances soient en état running

for instance_id in $instance_ids; do
aws ec2 wait instance-running --instance-ids "$instance_id"
done

# Récupérer et afficher les IPs publiques

for instance_id in $instance_ids; do
public_ip=$(aws ec2 describe-instances 
--instance-ids "$instance_id" 
--output text 
--query 'Reservations[*].Instances[*].PublicIpAddress')
echo "Instance ID = $instance_id, Security Group ID = $security_group_id, Public IP = $public_ip"
done

echo "Pour vous connecter en SSH :"
for instance_id in $instance_ids; do
public_ip=$(aws ec2 describe-instances 
--instance-ids "$instance_id" 
--output text 
--query 'Reservations[*].Instances[*].PublicIpAddress')
echo "ssh -i $HOME/$KEY_NAME.pem ec2-user@$public_ip"
done
