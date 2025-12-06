# Deployment Guide

## Local Deployment (Minikube)

### Prerequisites
```bash
# Check installations
minikube version
kubectl version
docker --version
```

### Step 1: Start Minikube

```bash
# Start cluster with sufficient resources
minikube start \
  --driver=docker \
  --cpus=4 \
  --memory=8192 \
  --disk-size=20gb

# Verify
minikube status
kubectl get nodes
```

### Step 2: Build Docker Images

```bash
# Build backend
docker build -t devops-final-backend:latest ./final-project/backend

# Build frontend
docker build -t devops-final-frontend:latest ./final-project/frontend

# Verify
docker images | grep devops-final
```

### Step 3: Deploy to Minikube

```bash
# Using Kustomize (recommended)
kubectl apply -k final-project/kubernetes/

# Or using kubectl directly
kubectl apply -f final-project/kubernetes/database/
kubectl apply -f final-project/kubernetes/backend/
kubectl apply -f final-project/kubernetes/frontend/

# Verify deployment
kubectl get all
kubectl get pods -o wide
```

### Step 4: Wait for Ready State

```bash
# Watch pods
kubectl get pods -w

# Check specific pod
kubectl describe pod <pod-name>

# Wait for all to be ready
kubectl wait --for=condition=Ready pod -l app=backend --timeout=300s
kubectl wait --for=condition=Ready pod -l app=frontend --timeout=300s
kubectl wait --for=condition=Ready pod -l app=postgres --timeout=300s
```

### Step 5: Access Application

```bash
# Terminal 1: Frontend port-forward
kubectl port-forward svc/frontend-service 3000:80

# Terminal 2: Backend port-forward
kubectl port-forward svc/backend-service 8000:8000

# Terminal 3: Open browser
open http://localhost:3000
```

### Step 6: Monitor & Troubleshoot

```bash
# View all resources
kubectl get all

# View pod logs
kubectl logs -f deployment/backend-deployment
kubectl logs -f deployment/frontend-deployment
kubectl logs -f deployment/postgres-deployment

# Check pod events
kubectl describe pod <pod-name>

# Port forward to database
kubectl port-forward svc/postgres-service 5432:5432
# Then: psql -h localhost -U devops_user -d devops_db
```

---

## Cloud Deployment (AWS EKS)

### Prerequisites
```bash
# Install AWS CLI
aws --version

# Configure AWS credentials
aws configure

# Install eksctl
eksctl version

# Install Helm (optional)
helm version
```

### Step 1: Create EKS Cluster

```bash
# Create cluster
eksctl create cluster \
  --name devops-final \
  --version 1.27 \
  --region us-east-1 \
  --nodes 3 \
  --node-type t3.medium

# Wait for cluster creation (10-15 minutes)

# Verify
eksctl get cluster --name devops-final
```

### Step 2: Configure kubectl

```bash
# Update kubeconfig
aws eks update-kubeconfig \
  --name devops-final \
  --region us-east-1

# Verify
kubectl get nodes
kubectl get pods --all-namespaces
```

### Step 3: Push Docker Images to ECR

```bash
# Create ECR repository
aws ecr create-repository --repository-name devops-final-backend --region us-east-1
aws ecr create-repository --repository-name devops-final-frontend --region us-east-1

# Get ECR login
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Tag and push backend
docker tag devops-final-backend:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/devops-final-backend:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/devops-final-backend:latest

# Tag and push frontend
docker tag devops-final-frontend:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/devops-final-frontend:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/devops-final-frontend:latest
```

### Step 4: Update Kubernetes Manifests

```bash
# Update image references in kubernetes/backend/backend-deployment.yaml
# Change: image: devops-final-backend:latest
# To: image: $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/devops-final-backend:latest

# Do the same for frontend

# Apply manifests
kubectl apply -k final-project/kubernetes/
```

### Step 5: Setup RDS for Production

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier devops-final-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --allocated-storage 20 \
  --db-name devops_db \
  --master-username devops_user \
  --master-user-password "YourSecurePassword123!" \
  --publicly-accessible false

# Wait for instance to be available
aws rds describe-db-instances --db-instance-identifier devops-final-db

# Update database connection string in backend secrets
```

### Step 6: Deploy Application

```bash
# Deploy
kubectl apply -k final-project/kubernetes/

# Verify
kubectl get all
kubectl get pods -o wide
```

---

## Cloud Deployment (Azure AKS)

### Prerequisites
```bash
# Install Azure CLI
az --version

# Login to Azure
az login

# Install kubectl
kubectl version
```

### Step 1: Create AKS Cluster

```bash
# Create resource group
az group create \
  --name devops-final-rg \
  --location eastus

# Create AKS cluster
az aks create \
  --resource-group devops-final-rg \
  --name devops-final-aks \
  --node-count 3 \
  --vm-set-type VirtualMachineScaleSets \
  --load-balancer-sku standard

# Wait for cluster creation
```

### Step 2: Configure kubectl

```bash
# Get credentials
az aks get-credentials \
  --resource-group devops-final-rg \
  --name devops-final-aks

# Verify
kubectl get nodes
```

### Step 3: Setup Azure Container Registry

```bash
# Create ACR
az acr create \
  --resource-group devops-final-rg \
  --name devopsfinalacr \
  --sku Basic

# Login to ACR
az acr login --name devopsfinalacr

# Tag and push images
docker tag devops-final-backend:latest \
  devopsfinalacr.azurecr.io/devops-final-backend:latest
docker push devopsfinalacr.azurecr.io/devops-final-backend:latest

docker tag devops-final-frontend:latest \
  devopsfinalacr.azurecr.io/devops-final-frontend:latest
docker push devopsfinalacr.azurecr.io/devops-final-frontend:latest
```

### Step 4: Create Azure Database for PostgreSQL

```bash
# Create PostgreSQL server
az postgres server create \
  --resource-group devops-final-rg \
  --name devops-final-db \
  --location eastus \
  --admin-user devops_user \
  --admin-password "YourSecurePassword123!" \
  --sku-name B_Gen5_1 \
  --storage-size 51200 \
  --version 12

# Update firewall rules
az postgres server firewall-rule create \
  --resource-group devops-final-rg \
  --server devops-final-db \
  --name AllowAKS \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 255.255.255.255
```

### Step 5: Deploy Application

```bash
# Update image references to ACR
# Then deploy
kubectl apply -k final-project/kubernetes/

# Verify
kubectl get all
```

---

## Post-Deployment

### Verify Deployment

```bash
# Check all resources
kubectl get all -o wide

# Check pod status
kubectl get pods

# Check services
kubectl get svc

# Check persistent volumes
kubectl get pvc

# Check ConfigMaps and Secrets
kubectl get configmap
kubectl get secret
```

### Database Initialization

```bash
# Get PostgreSQL pod
POD=$(kubectl get pod -l app=postgres -o jsonpath='{.items[0].metadata.name}')

# Connect and initialize
kubectl exec -it $POD -- psql -U devops_user -d devops_db

# Or from outside cluster (with port-forward)
kubectl port-forward svc/postgres-service 5432:5432
psql -h localhost -U devops_user -d devops_db
```

### Monitoring

```bash
# View logs
kubectl logs -f deployment/backend-deployment
kubectl logs -f deployment/frontend-deployment

# Check resource usage
kubectl top pods
kubectl top nodes

# Watch deployments
kubectl get deployments -w
```

---

## Cleanup

### Delete Minikube Resources

```bash
# Delete all Kubernetes resources
kubectl delete -k final-project/kubernetes/

# Or delete individual components
kubectl delete deployment --all
kubectl delete svc --all
kubectl delete pvc --all

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

### Delete EKS Resources

```bash
# Delete Kubernetes resources
kubectl delete -k final-project/kubernetes/

# Delete EKS cluster
eksctl delete cluster --name devops-final --region us-east-1

# Delete ECR repositories
aws ecr delete-repository \
  --repository-name devops-final-backend \
  --force --region us-east-1

# Delete RDS instance
aws rds delete-db-instance \
  --db-instance-identifier devops-final-db \
  --skip-final-snapshot
```

### Delete AKS Resources

```bash
# Delete Kubernetes resources
kubectl delete -k final-project/kubernetes/

# Delete resource group (all resources)
az group delete --name devops-final-rg --yes
```

---

**Last Updated**: December 2024
