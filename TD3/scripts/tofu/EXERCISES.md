# Exercices Terraform - TD3 Section 5

## Exercise 7: Que se passe-t-il si on lance terraform apply après destruction ?

### Réponse:

Après `terraform destroy`, si on lance `terraform apply`:

1. **Terraform recréera les ressources** à partir du code Terraform
2. Les ressources seront créées avec de **nouvelles configurations** (nouvelles IPs, etc.)
3. **Le state file** sera mis à jour avec les nouvelles ressources

### Exemple:
```
terraform destroy   # Destroy les 2 ressources
terraform apply     # Recrée les 2 ressources avec de nouvelles IPs
```

**Raison** : Terraform compare le state file avec le code Terraform. Si les ressources n'existent pas dans le state file, Terraform les recrée.

### Démonstration:

1. Voir l'état actuel:
```bash
terraform state list
# aws_instance.sample_app
# aws_security_group.sample_app
```

2. Destroyer:
```bash
terraform destroy -auto-approve
# aws_security_group.sample_app destroyed
# aws_instance.sample_app destroyed
```

3. Relancer apply:
```bash
terraform apply -auto-approve
# aws_security_group.sample_app created
# aws_instance.sample_app created
# Nouvelle IP publique!
```

---

## Exercise 8: Déployer plusieurs instances EC2

### Solution avec count

Modifier `variables.tf`:

```hcl
variable "instance_count" {
  description = "Number of instances to create"
  type        = number
  default     = 1
}
```

Modifier `main.tf`:

```hcl
resource "aws_instance" "sample_app" {
  count                  = var.instance_count
  ami                    = var.ami_id
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.sample_app.id]
  user_data              = file("${path.module}/user-data.sh")

  tags = {
    Name = "sample-app-tofu-${count.index + 1}"
    Test = "update"
  }
}
```

Modifier `outputs.tf`:

```hcl
output "instance_ids" {
  description = "IDs of the EC2 instances"
  value       = aws_instance.sample_app[*].id
}

output "public_ips" {
  description = "Public IPs of the EC2 instances"
  value       = aws_instance.sample_app[*].public_ip
}

output "application_urls" {
  description = "URLs to access the applications"
  value       = [for ip in aws_instance.sample_app[*].public_ip : "http://${ip}:8080"]
}
```

Modifier `terraform.tfvars`:

```hcl
ami_id          = "ami-0dc529b866af9ec38"
instance_count  = 3  # Créer 3 instances
```

### Appliquer:

```bash
terraform plan
# Plan: 2 to add (+ 2 instances supplémentaires)

terraform apply -auto-approve
# Instance 1: i-xxxxx (IP: 1.2.3.4)
# Instance 2: i-yyyyy (IP: 1.2.3.5)
# Instance 3: i-zzzzz (IP: 1.2.3.6)
```

### Alternative avec for_each

```hcl
variable "instances" {
  type = map(object({
    instance_type = string
    tag_name      = string
  }))
  default = {
    "app-1" = { instance_type = "t3.micro", tag_name = "app-1" }
    "app-2" = { instance_type = "t3.micro", tag_name = "app-2" }
    "app-3" = { instance_type = "t3.small", tag_name = "app-3" }
  }
}

resource "aws_instance" "sample_app" {
  for_each               = var.instances
  ami                    = var.ami_id
  instance_type          = each.value.instance_type
  vpc_security_group_ids = [aws_security_group.sample_app.id]
  user_data              = file("${path.module}/user-data.sh")

  tags = {
    Name = each.value.tag_name
    Test = "update"
  }
}
```

### Avantages de count vs for_each

| count | for_each |
|-------|----------|
| Indices numériques | Clés nommées |
| Ajouter au début = réindex | Ajouter = pas d'impact |
| Simple | Plus flexible |

---

## Résumé

✅ **Exercise 7** : `terraform apply` après `destroy` recrée tout
✅ **Exercise 8** : Utiliser `count` ou `for_each` pour plusieurs instances

