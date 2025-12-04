# Part 3 : Container Orchestration with Docker and Kubernetes 🐳☸️

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Part 3.1: Building and Running Docker Images Locally](#part-31-building-and-running-docker-images-locally)
4. [Part 3.2: Deploying to Local Kubernetes Cluster](#part-32-deploying-to-local-kubernetes-cluster)
5. [Part 3.3: Rolling Updates](#part-33-rolling-updates)
6. [Project Structure](#project-structure)
7. [Cleanup](#cleanup)
8. [Conclusion](#conclusion)

---

## 📖 Overview

In this part, we explore **container orchestration** using Docker and Kubernetes. We'll:

- Build Docker images for a sample Node.js application
- Deploy the application to a local Kubernetes cluster (minikube)
- Implement rolling updates with zero-downtime deployments
- Practice version management and rollback strategies

**Key Learning Outcomes:**
- ✅ Docker containerization
- ✅ Kubernetes deployment and service management
- ✅ Rolling updates and zero-downtime deployments
- ✅ Container orchestration best practices

---

## 🔧 Prerequisites

### Required Tools

```bash
# Docker
docker --version
# Docker version 28.2.2 or higher

# Kubernetes
kubectl version --client
# Client Version: v1.34.2 or higher

# minikube (for local Kubernetes)
minikube version
# minikube version: v1.37.0 or higher

# Git
git --version
```

### Installation Commands

```bash
# Install Docker (if not installed)
# Follow: https://docs.docker.com/engine/install/ubuntu/

# Install kubectl
sudo snap install kubectl --classic

# Install minikube
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Add user to docker group (to avoid sudo)
sudo usermod -aG docker $USER
newgrp docker
```

---

## 📦 Part 3.1: Building and Running Docker Images Locally

### Step 1.1: Set Up the Working Directory

```bash
mkdir -p devops_base/TD3/scripts/docker
cd devops_base/TD3/scripts/docker
```

### Step 1.2: Create the Sample Application

**File: `app.js` (Version 1)**

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('DevOps Base!\n');
});

server.listen(8080, () => {
  console.log('Application démarrée sur le port 8080');
});
```

### Step 1.3: Create the Dockerfile

**File: `Dockerfile`**

```dockerfile
FROM node:current-alpine

WORKDIR /usr/src/app

COPY app.js .

EXPOSE 8080

CMD ["node", "app.js"]
```

### Step 1.4: Build the Docker Image

```bash
docker build -t sample-app:v1 .
```

**Expected Output:**
```
Successfully built <hash>
Successfully tagged sample-app:v1
```

### Step 1.5: Run the Docker Container Locally

```bash
# Terminal 1
docker run -p 8080:8080 --name sample-app --rm sample-app:v1
```

**Expected Output:**
```
Application démarrée sur le port 8080
```

### Step 1.6: Test the Application

```bash
# Terminal 2
curl http://localhost:8080

# Expected Output:
# DevOps Base!
```

---

## ☸️ Part 3.2: Deploying to Local Kubernetes Cluster

### Step 2.1: Start minikube

```bash
minikube start --driver=docker
```

**Expected Output:**
```
😄  minikube v1.37.0 on Ubuntu 24.04
✨  Using the docker driver
🏄  Done! kubectl is now configured to use "minikube" cluster
```

### Step 2.2: Verify Kubernetes is Running

```bash
kubectl get nodes
```

**Expected Output:**
```
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   37s   v1.34.0
```

### Step 2.3: Load Docker Image into minikube

```bash
minikube image load sample-app:v1
```

### Step 2.4: Create Kubernetes Deployment

**File: `sample-app-deployment.yaml`**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-app-deployment
  labels:
    app: sample-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
    spec:
      containers:
      - name: sample-app
        image: sample-app:v1
        imagePullPolicy: Never
        ports:
        - containerPort: 8080
```

### Step 2.5: Apply the Deployment

```bash
kubectl apply -f sample-app-deployment.yaml
```

### Step 2.6: Verify Pods are Running

```bash
kubectl get pods
```

**Expected Output:**
```
NAME                                     READY   STATUS    RESTARTS   AGE
sample-app-deployment-6b68c785f5-jlq69   1/1     Running   0          12s
sample-app-deployment-6b68c785f5-pqqst   1/1     Running   0          12s
sample-app-deployment-6b68c785f5-sgtlk   1/1     Running   0          12s
```

### Step 2.7: Create Kubernetes Service

**File: `sample-app-service.yaml`**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: sample-app-service
  labels:
    app: sample-app
spec:
  type: LoadBalancer
  selector:
    app: sample-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

### Step 2.8: Apply the Service

```bash
kubectl apply -f sample-app-service.yaml
```

### Step 2.9: Access the Application

```bash
# Terminal 1: Port-forward
kubectl port-forward service/sample-app-service 8080:80

# Terminal 2: Test
curl http://localhost:8080

# Expected Output:
# DevOps Base!
```

---

## 🔄 Part 3.3: Rolling Updates

### Step 3.1: Update the Application Code

**File: `app.js` (Version 2)**

```javascript
const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('🚀 DevOps Base v2 - Rolling Update Works!\n');
});

server.listen(8080, () => {
  console.log('Application v2 démarrée sur le port 8080');
});
```

### Step 3.2: Build New Docker Image

```bash
docker build -t sample-app:v2 .
```

### Step 3.3: Load New Image into minikube

```bash
minikube image load sample-app:v2
```

### Step 3.4: Update Deployment Manifest

**File: `sample-app-deployment.yaml` (Updated)**

```yaml
# Change image from sample-app:v1 to sample-app:v2
spec:
  containers:
  - name: sample-app
    image: sample-app:v2
    imagePullPolicy: Never
```

### Step 3.5: Apply Updated Deployment

```bash
kubectl apply -f sample-app-deployment.yaml
```

### Step 3.6: Monitor Rolling Update

```bash
kubectl rollout status deployment/sample-app-deployment
```

**Expected Output:**
```
Waiting for deployment "sample-app-deployment" to rollout
deployment "sample-app-deployment" successfully rolled out
```

### Step 3.7: Test Updated Application

```bash
curl http://localhost:8080

# Expected Output:
# 🚀 DevOps Base v2 - Rolling Update Works!
```

### Step 3.8: View Rollout History

```bash
kubectl rollout history deployment/sample-app-deployment
```

**Expected Output:**
```
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
```

### Step 3.9: Rollback to Previous Version

```bash
kubectl rollout undo deployment/sample-app-deployment

# Verify
kubectl rollout status deployment/sample-app-deployment

# Test
curl http://localhost:8080

# Expected Output:
# DevOps Base!
```

### Step 3.10: Re-Deploy Latest Version

```bash
kubectl apply -f sample-app-deployment.yaml

# Verify
curl http://localhost:8080

# Expected Output:
# 🚀 DevOps Base v2 - Rolling Update Works!
```

---

## �� Project Structure

```
devops_base/
├── TD3/
│   ├── scripts/
│   │   ├── docker/
│   │   │   ├── app.js              (v1 & v2)
│   │   │   └── Dockerfile
│   │   ├── kubernetes/
│   │   │   ├── sample-app-deployment.yaml
│   │   │   └── sample-app-service.yaml
│   │   ├── tofu/                   (Part 2 - AWS)
│   │   │   └── live/
│   │   │       └── asg-sample/
│   │   └── README_PART3.md         (This file)
│   └── ...
└── ...
```

---

## 🧹 Cleanup

### Step 1: Delete Kubernetes Resources

```bash
cd TD3/scripts/kubernetes

kubectl delete deployment sample-app-deployment
kubectl delete service sample-app-service
```

### Step 2: Stop minikube

```bash
minikube stop

# Optional: Delete minikube cluster
# minikube delete
```

### Step 3: Remove Docker Images

```bash
cd TD3/scripts/docker

docker rmi sample-app:v1 sample-app:v2
```

### Step 4: Verify Cleanup

```bash
kubectl get all              # Should be empty
minikube status              # Should be Stopped
docker images | grep sample  # Should be empty
```

---

## 📚 Key Concepts

### Docker
- **Image**: Lightweight, standalone, executable package
- **Container**: Runtime instance of an image
- **Dockerfile**: Recipe to build images
- **Registry**: Repository to store/share images

### Kubernetes
- **Pod**: Smallest deployable unit (usually 1 container)
- **Deployment**: Manages replicas of pods
- **Service**: Network abstraction to expose pods
- **Rolling Update**: Update pods gradually without downtime

### Rolling Updates
- Gradually replace old pods with new ones
- Maintain application availability during updates
- Allow easy rollback if issues occur

---

## ✅ Testing Checklist

- [ ] Docker image builds successfully
- [ ] Container runs locally on port 8080
- [ ] minikube starts without errors
- [ ] 3 Kubernetes pods are running
- [ ] Service is accessible via localhost:8080
- [ ] Rolling update completes without downtime
- [ ] Application responds correctly (v1 and v2)
- [ ] Rollback works as expected
- [ ] Resources are cleaned up after completion

---

## 🎯 Learning Outcomes

By completing this part, you've learned:

✅ **Container Basics**
- Build Docker images from Dockerfile
- Run containers locally with port mapping
- Understand container networking

✅ **Kubernetes Fundamentals**
- Deploy applications to Kubernetes
- Create and manage services
- Scale applications with replicas

✅ **Rolling Updates**
- Update applications with zero downtime
- Monitor deployment progress
- Rollback to previous versions

✅ **Best Practices**
- Use health checks for reliability
- Implement gradual updates
- Test before production deployment

---

## 📖 Additional Resources

- **Docker Documentation**: https://docs.docker.com/
- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **minikube Documentation**: https://minikube.sigs.k8s.io/
- **Container Best Practices**: https://docs.docker.com/develop/dev-best-practices/

---

## 🚀 Next Steps

### Option A: Part 4 - EKS & ECR (AWS)
⚠️ **Note**: EKS incurs costs (~$0.10/hour for control plane)

Deploy to AWS Elastic Kubernetes Service (EKS):
- Create EKS cluster with Terraform
- Push images to Amazon ECR
- Deploy application to EKS

### Option B: Part 5 - AWS Lambda (Serverless)
✅ **Recommended**: Uses AWS Free Tier

Deploy serverless functions without managing infrastructure.

---

## 📝 Troubleshooting

### Problem: `permission denied while trying to connect to Docker daemon`
**Solution:**
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Problem: `ErrImageNeverPull` in Kubernetes pods
**Solution:**
```bash
# Ensure image is loaded into minikube
minikube image load sample-app:v1
```

### Problem: Port 8080 already in use
**Solution:**
```bash
# Kill existing port-forward
pkill -f "kubectl port-forward"

# Or use a different port
kubectl port-forward service/sample-app-service 8081:80
```

---

## 📞 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review Kubernetes/Docker official documentation
3. Check GitHub issues for similar problems
4. Contact the project maintainer

---

## ✨ Conclusion

In Part 3, you've mastered:
- **Container orchestration** with Docker and Kubernetes
- **Zero-downtime deployments** using rolling updates
- **Application versioning** and rollback strategies
- **Local Kubernetes development** with minikube

You're now ready to deploy containerized applications in production environments!

�� **Part 3 Complete!**

---

**Last Updated**: December 4, 2025  
**Status**: ✅ Complete and Tested  
**Version**: 1.0
