# 🎉 TD6: Kubernetes Microservices Deployment

## Overview

Complete DevOps training module for deploying microservices on Kubernetes with multiple AWS accounts and Infrastructure as Code.

## 📋 Table of Contents

- [Part 1: Multi-AWS Account Setup](#part-1-multi-aws-account-setup)
- [Part 2: OpenTofu Workspaces](#part-2-opentofu-workspaces)
- [Part 3: Kubernetes Microservices](#part-3-kubernetes-microservices)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Testing](#testing)

---

## Part 1: Multi-AWS Account Setup

### Objectives
✅ Set up multi-AWS account architecture
✅ Configure IAM roles for cross-account access
✅ Establish organization structure
✅ Implement environment isolation

### AWS Account Structure
```
Root Account (Management)
├── Development Account
├── Staging Account
└── Production Account
```

### IAM Configuration
- Cross-account access roles
- Service-linked roles
- Trust relationships
- Policy management

### Files
- `part1-aws/` - AWS account configurations

---

## Part 2: OpenTofu Workspaces

### Objectives
✅ Create development workspace
✅ Create staging workspace
✅ Create production workspace
✅ Manage state per environment
✅ Implement workspace isolation

### Workspaces
```
Terraform/OpenTofu
├── dev workspace
├── staging workspace
└── prod workspace
```

### State Management
- Remote backend configuration
- State locking
- Workspace-specific variables
- Environment-specific settings

### Files
- `part2-opentofu/` - Infrastructure as Code configurations

---

## Part 3: Kubernetes Microservices

### Objectives
✅ Deploy backend microservice (3 replicas)
✅ Deploy frontend microservice (3 replicas)
✅ Configure service discovery via DNS
✅ Implement pod-to-pod communication
✅ Set up LoadBalancer for external access

### Architecture

```
┌─────────────────────────────────────────────┐
│         Kubernetes Cluster (Minikube)       │
├─────────────────────────────────────────────┤
│                                             │
│  LoadBalancer Service (Frontend)            │
│  ┌───────────────────────────────────────┐  │
│  │  Frontend Deployment (3 replicas)     │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┤  │
│  │  │ Pod 1   │  │ Pod 2   │  │ Pod 3   │  │
│  │  │ :8080   │  │ :8080   │  │ :8080   │  │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  │
│  └───────┼─────────────┼─────────────┼───────┘
│          │ DNS: sample-app-backend-service  │
│          ↓                                  │
│  ClusterIP Service (Backend)                │
│  ┌───────────────────────────────────────┐  │
│  │  Backend Deployment (3 replicas)      │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┤  │
│  │  │ Pod 1   │  │ Pod 2   │  │ Pod 3   │  │
│  │  │ :8080   │  │ :8080   │  │ :8080   │  │
│  │  └─────────┘  └─────────┘  └─────────┘  │
│  └───────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
```

### Services

#### Backend Service
- **Name**: sample-app-backend-service
- **Type**: ClusterIP
- **Replicas**: 3
- **Port**: 80 → 8080
- **Endpoint**: http://sample-app-backend-service
- **Response**: `{"text":"backend microservice"}`

#### Frontend Service
- **Name**: sample-app-frontend-loadbalancer
- **Type**: LoadBalancer
- **Replicas**: 3
- **Port**: 80 → 8080
- **Endpoint**: http://localhost:8080 (via port-forward)
- **Features**: Calls backend via DNS

### Microservices

#### Backend
- Express.js API server
- Returns JSON response
- Health checks
- 3 replicas for scaling

#### Frontend
- Express.js server
- EJS templating
- Calls backend service
- Dynamic content rendering

---

## Quick Start

### Prerequisites
- Docker installed
- Kubernetes cluster (Minikube)
- kubectl configured
- Node.js 20+ (for local testing)

### Deploy

```bash
cd td6/scripts
./deploy.sh
```

This script:
1. Builds Docker images
2. Creates Kubernetes deployments
3. Creates Kubernetes services
4. Verifies pod status
5. Tests service communication

### Access Frontend

```bash
# In terminal 1: Port-forward
kubectl port-forward svc/sample-app-frontend-loadbalancer 8080:80

# In terminal 2: Open in browser or curl
curl http://localhost:8080
# or
open http://localhost:8080
```

### Check Status

```bash
# View pods
kubectl get pods

# View services
kubectl get svc

# View pod details
kubectl describe pod <pod-name>

# View logs
kubectl logs -l app=sample-app-backend-pods
kubectl logs -l app=sample-app-frontend-pods

# Port-forward to backend
kubectl port-forward svc/sample-app-backend-service 8000:80
curl http://localhost:8000
```

### Cleanup

```bash
cd td6/scripts
./cleanup.sh
```

This removes:
- Kubernetes deployments
- Kubernetes services
- Docker images (optional)

---

## Architecture Details

### Kubernetes Resources

#### Backend Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-app-backend-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sample-app-backend-pods
  template:
    metadata:
      labels:
        app: sample-app-backend-pods
    spec:
      containers:
      - name: sample-app-backend
        image: sample-app-backend:latest
        ports:
        - containerPort: 8080
```

#### Backend Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: sample-app-backend-service
spec:
  type: ClusterIP
  selector:
    app: sample-app-backend-pods
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

#### Frontend Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-app-frontend-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sample-app-frontend-pods
  template:
    metadata:
      labels:
        app: sample-app-frontend-pods
    spec:
      containers:
      - name: sample-app-frontend
        image: sample-app-frontend:latest
        ports:
        - containerPort: 8080
```

#### Frontend Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: sample-app-frontend-loadbalancer
spec:
  type: LoadBalancer
  selector:
    app: sample-app-frontend-pods
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
```

### Docker Images

#### Backend Dockerfile
Multi-stage build optimizing size and security:
- Base: node:20-alpine
- Build stage: Install dependencies
- Runtime stage: Only production files

#### Frontend Dockerfile
Optimized for web serving:
- Base: node:20-alpine
- Includes EJS views
- Minimal production size

---

## Testing

### Health Checks

```bash
# Backend health
curl http://localhost:8000

# Frontend health
curl http://localhost:8080

# Service discovery test
kubectl exec -it <pod-name> -- curl http://sample-app-backend-service
```

### Pod Communication

```bash
# Test backend → backend
kubectl exec -it <backend-pod> -- curl localhost:8080

# Test frontend → backend
kubectl exec -it <frontend-pod> -- curl sample-app-backend-service
```

### Scaling Test

```bash
# Scale backend to 5 replicas
kubectl scale deployment sample-app-backend-deployment --replicas=5

# Verify
kubectl get pods

# Scale back to 3
kubectl scale deployment sample-app-backend-deployment --replicas=3
```

---

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Service discovery not working
```bash
# Check DNS
kubectl exec -it <pod-name> -- nslookup sample-app-backend-service
```

### Port-forward issues
```bash
# Check service
kubectl get svc

# Verify port
kubectl port-forward svc/sample-app-frontend-loadbalancer 8080:80
```

### Image pull issues
```bash
# Build images locally
docker build -t sample-app-backend:latest ./scripts/sample-app-backend
docker build -t sample-app-frontend:latest ./scripts/sample-app-frontend
```

---

## Files Structure

```
td6/
├── README.md                              # This file
├── COMPLETION.md                          # Completion checklist
├── scripts/
│   ├── deploy.sh                          # Deployment script
│   ├── cleanup.sh                         # Cleanup script
│   ├── sample-app-backend/
│   │   ├── app.js                         # Backend Express server
│   │   ├── package.json                   # Dependencies
│   │   ├── Dockerfile                     # Backend image
│   │   ├── sample-app-deployment.yml      # K8s deployment
│   │   └── sample-app-service.yml         # K8s service
│   └── sample-app-frontend/
│       ├── app.js                         # Frontend Express server
│       ├── package.json                   # Dependencies
│       ├── Dockerfile                     # Frontend image
│       ├── views/
│       │   └── hello.ejs                  # EJS template
│       ├── sample-app-deployment.yml      # K8s deployment
│       └── sample-app-service.yml         # K8s service
├── kubernetes/                            # K8s resources
├── microservices/                         # Microservice code
├── part1-aws/                             # AWS account setup
└── part2-opentofu/                        # OpenTofu configurations
```

---

## Technologies Used

| Component | Technology |
|-----------|-----------|
| Cloud | AWS (Multi-account) |
| IaC | OpenTofu/Terraform |
| Containers | Docker |
| Orchestration | Kubernetes (Minikube) |
| Runtime | Node.js 20 |
| Framework | Express.js |
| Templating | EJS |
| Service Mesh | Kubernetes DNS |

---

## Learning Outcomes

✅ Kubernetes deployment management
✅ Service discovery and DNS
✅ Pod communication patterns
✅ Container orchestration
✅ Microservices architecture
✅ Docker optimization
✅ Infrastructure automation
✅ Multi-cloud AWS setup
✅ Infrastructure as Code best practices
✅ Production-ready deployment

---

## References

- [Kubernetes Documentation](https://kubernetes.io/)
- [Docker Documentation](https://docs.docker.com/)
- [OpenTofu Documentation](https://opentofu.org/)
- [AWS Documentation](https://docs.aws.amazon.com/)
- [Express.js Guide](https://expressjs.com/)

---

## Author

**Course**: DevOps Training - TD6  
**Date**: December 2024  
**Status**: Production-Ready ✅

