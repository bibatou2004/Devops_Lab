# 🎯 DevOps Final Project: CI/CD Data Pipeline on Kubernetes

**Author**: Badr TAJINI - DevOps Data  
**School**: ESIEE 2025  
**Status**: Production Ready ✅  
**Last Updated**: December 2024

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Features](#features)
- [Deployment](#deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [API Documentation](#api-documentation)
- [Database](#database)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This is a **complete DevOps project** demonstrating:

✅ **Full-Stack Application**: FastAPI Backend + React Frontend  
✅ **Database Integration**: PostgreSQL with CRUD operations  
✅ **Container Architecture**: Docker & Kubernetes  
✅ **CI/CD Automation**: GitHub Actions pipeline  
✅ **Infrastructure as Code**: Kubernetes manifests & Kustomization  
✅ **Best Practices**: Health checks, rolling updates, security scanning

### Project Goal

Build and deploy a **Task Management Application** with:
- Automated CI/CD pipeline
- Kubernetes orchestration
- Database persistence
- Health monitoring
- Production-ready setup

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Repository                         │
│              (Main & Develop Branches)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│            GitHub Actions CI/CD Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│ 1. Code Checkout & Analysis                                 │
│ 2. Backend: Python Tests & Linting                          │
│ 3. Frontend: Node.js Build & Tests                          │
│ 4. Security: Trivy Vulnerability Scanning                   │
│ 5. Build: Docker Images (Backend & Frontend)                │
│ 6. Push: Registry (Docker Hub)                              │
│ 7. Deploy: Kubernetes (Staging/Production)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│              Kubernetes Cluster (Minikube)                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Frontend Pod (3 replicas)                            │   │
│  │ - React 18 Application                              │   │
│  │ - Port 3000                                         │   │
│  │ - Load Balanced Service                             │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                         │
│                   ↓                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Backend Service (ClusterIP)                          │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ Backend Pod (3 replicas)                             │   │
│  │ - FastAPI Application                               │   │
│  │ - Port 8000                                         │   │
│  │ - Health Checks Enabled                             │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                         │
│                   ↓                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ PostgreSQL Service (ClusterIP)                       │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ PostgreSQL Pod (1 replica)                           │   │
│  │ - Database: devops_db                               │   │
│  │ - Port 5432                                         │   │
│  │ - Persistent Volume (5Gi)                           │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
1. User Interaction
   Browser → Frontend (React)

2. API Call
   Frontend → Backend Service (FastAPI)

3. Database Operation
   Backend → PostgreSQL Database

4. Response Flow
   Database → Backend → Frontend → Browser
```

---

## 🛠️ Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Frontend** | React | 18.2 |
| | Node.js | 18 |
| **Backend** | FastAPI | 0.104 |
| | Python | 3.11 |
| | SQLAlchemy | 2.0 |
| **Database** | PostgreSQL | 15 |
| **Containers** | Docker | Latest |
| **Orchestration** | Kubernetes | 1.27+ |
| **Local K8s** | Minikube | Latest |
| **CI/CD** | GitHub Actions | Latest |
| **Registry** | Docker Hub | - |

---

## 📦 Prerequisites

### Required Software

```bash
# Check versions
python --version           # Python 3.11+
node --version            # Node.js 18+
docker --version          # Docker 20.10+
minikube version          # Minikube latest
kubectl version           # Kubernetes CLI
git --version             # Git 2.30+
```

### Installation

**macOS**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install tools
brew install python node docker minikube kubectl git
```

**Ubuntu/Debian**
```bash
sudo apt update
sudo apt install -y python3 python3-pip nodejs npm docker.io git
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

**Windows**
```powershell
# Using Chocolatey
choco install python nodejs docker-desktop minikube kubernetes-cli git

# Or manual installation from official websites
```

### GitHub Secrets (Required for CI/CD)

Set these secrets in your GitHub repository settings:

```
DOCKER_USERNAME          → Your Docker Hub username
DOCKER_PASSWORD          → Your Docker Hub password
KUBE_CONFIG_STAGING      → Base64 encoded kubeconfig (staging)
KUBE_CONFIG_PROD         → Base64 encoded kubeconfig (production)
SLACK_WEBHOOK            → Slack webhook URL (optional)
```

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/your-username/devops-final-project.git
cd devops-final-project
```

### 2. Start Minikube

```bash
# Start cluster
minikube start --driver=docker --cpus=4 --memory=8192

# Verify
minikube status
kubectl get nodes
```

### 3. Build Docker Images

```bash
# Backend
cd final-project/backend
docker build -t devops-final-backend:latest .

# Frontend
cd ../frontend
docker build -t devops-final-frontend:latest .
```

### 4. Deploy to Kubernetes

```bash
cd ../..

# Option 1: Using kubectl directly
kubectl apply -f final-project/kubernetes/database/
kubectl apply -f final-project/kubernetes/backend/
kubectl apply -f final-project/kubernetes/frontend/

# Option 2: Using Kustomize
kubectl apply -k final-project/kubernetes/

# Verify deployment
kubectl get all
kubectl get pods -o wide
```

### 5. Access Application

```bash
# Port-forward frontend
kubectl port-forward svc/frontend-service 3000:80 &

# Port-forward backend
kubectl port-forward svc/backend-service 8000:8000 &

# Open in browser
open http://localhost:3000
# or
curl http://localhost:3000
```

### 6. Monitor Deployment

```bash
# Watch pods
kubectl get pods -w

# View logs
kubectl logs -f deployment/backend-deployment
kubectl logs -f deployment/frontend-deployment
kubectl logs -f deployment/postgres-deployment

# Check services
kubectl get svc -o wide

# Check persistent volumes
kubectl get pvc
```

### 7. Cleanup

```bash
# Stop port-forward
pkill -f port-forward

# Delete all resources
kubectl delete -k final-project/kubernetes/

# Stop Minikube
minikube stop
```

---

## 📁 Project Structure

```
devops-final-project/
├── .github/
│   └── workflows/
│       ├── ci-cd-pipeline.yaml        # Main CI/CD workflow
│       ├── scheduled-checks.yaml       # Health check schedule
│       └── manual-deploy.yaml          # Manual deployment
│
├── final-project/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── main.py                # FastAPI main application
│   │   │   ├── database.py            # SQLAlchemy models
│   │   │   ├── schemas.py             # Pydantic schemas
│   │   │   └── crud.py                # Database operations
│   │   ├── tests/
│   │   │   └── test_api.py            # Unit tests
│   │   ├── requirements.txt           # Python dependencies
│   │   └── Dockerfile                 # Backend image
│   │
│   ├── frontend/
│   │   ├── src/
│   │   │   ├── App.jsx                # Main React component
│   │   │   └── App.css                # Styling
│   │   ├── public/
│   │   │   └── index.html             # HTML entry
│   │   ├── package.json               # Node dependencies
│   │   └── Dockerfile                 # Frontend image
│   │
│   ├── database/
│   │   └── schemas/
│   │       └── init.sql               # Database initialization
│   │
│   ├── kubernetes/
│   │   ├── database/
│   │   │   ├── postgres-configmap.yaml
│   │   │   ├── postgres-secret.yaml
│   │   │   ├── postgres-pvc.yaml
│   │   │   ├── postgres-deployment.yaml
│   │   │   └── postgres-service.yaml
│   │   ├── backend/
│   │   │   ├── backend-configmap.yaml
│   │   │   ├── backend-secret.yaml
│   │   │   ├── backend-deployment.yaml
│   │   │   └── backend-service.yaml
│   │   ├── frontend/
│   │   │   ├── frontend-configmap.yaml
│   │   │   ├── frontend-deployment.yaml
│   │   │   └── frontend-service.yaml
│   │   ├── ingress.yaml               # Ingress configuration
│   │   └── kustomization.yaml         # Kustomize config
│   │
│   ├── docs/
│   │   ├── ARCHITECTURE.md            # Architecture details
│   │   ├── API.md                     # API documentation
│   │   ├── DEPLOYMENT.md              # Deployment guide
│   │   ├── TESTING.md                 # Testing guide
│   │   └── TROUBLESHOOTING.md         # Troubleshooting
│   │
│   ├── scripts/
│   │   ├── deploy.sh                  # Deployment script
│   │   ├── cleanup.sh                 # Cleanup script
│   │   └── test.sh                    # Testing script
│   │
│   └── README.md                      # This file
│
└── docs/
    └── PROJECT_SUMMARY.md             # Project summary

```

---

## ✨ Features

### Frontend Features
- ✅ Create, Read, Update, Delete (CRUD) tasks
- ✅ Real-time statistics dashboard
- ✅ Responsive design
- ✅ Task completion tracking
- ✅ Automatic backend synchronization

### Backend Features
- ✅ RESTful API with FastAPI
- ✅ Database persistence with PostgreSQL
- ✅ Health check endpoints
- ✅ CRUD operations on tasks
- ✅ Statistics aggregation
- ✅ Error handling
- ✅ Logging

### DevOps Features
- ✅ Automated CI/CD pipeline
- ✅ Docker containerization
- ✅ Kubernetes orchestration
- ✅ Health checks & readiness probes
- ✅ Rolling updates
- ✅ Persistent volumes
- ✅ Security scanning
- ✅ Resource limits & requests

---

## 🚀 Deployment

### Local Deployment (Minikube)

```bash
# 1. Build images
docker build -t devops-final-backend:latest ./final-project/backend
docker build -t devops-final-frontend:latest ./final-project/frontend

# 2. Deploy
kubectl apply -k final-project/kubernetes/

# 3. Verify
kubectl get all
kubectl get pods -o wide

# 4. Access
kubectl port-forward svc/frontend-service 3000:80
open http://localhost:3000
```

### Cloud Deployment (AWS EKS / Azure AKS)

```bash
# 1. Create cluster
# AWS: eksctl create cluster --name devops-final --region us-east-1
# Azure: az aks create --resource-group myResourceGroup --name devopsCluster

# 2. Configure kubectl
# AWS: aws eks update-kubeconfig --name devops-final --region us-east-1
# Azure: az aks get-credentials --resource-group myResourceGroup --name devopsCluster

# 3. Deploy
kubectl apply -k final-project/kubernetes/

# 4. Check services
kubectl get svc
```

---

## 🔄 CI/CD Pipeline

### Pipeline Stages

```
1. Code Checkout
   ↓
2. Backend: Test & Lint
   ↓
3. Frontend: Build & Test
   ↓
4. Security: Trivy Scan
   ↓
5. Build Docker Images
   ↓
6. Push to Registry
   ↓
7. Deploy to Staging (develop branch)
   ↓
8. Deploy to Production (main branch)
   ↓
9. Smoke Tests & Notifications
```

### Manual Trigger

```bash
# Trigger manual deployment via GitHub UI
# Settings → Actions → Manual Deploy
# Or via CLI:
gh workflow run manual-deploy.yaml \
  -f environment=production \
  -f component=all \
  -f image_tag=latest
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000
```

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "backend",
  "database": "connected"
}
```

### Get All Tasks
```http
GET /tasks
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Learn Kubernetes",
    "description": "Master container orchestration",
    "completed": false,
    "created_at": "2024-12-06T10:00:00",
    "updated_at": "2024-12-06T10:00:00"
  }
]
```

### Create Task
```http
POST /tasks
Content-Type: application/json

{
  "title": "New Task",
  "description": "Task description"
}
```

**Response:** `201 Created`
```json
{
  "id": 5,
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2024-12-06T11:00:00",
  "updated_at": "2024-12-06T11:00:00"
}
```

### Update Task
```http
PUT /tasks/{task_id}
Content-Type: application/json

{
  "completed": true
}
```

### Delete Task
```http
DELETE /tasks/{task_id}
```

### Get Statistics
```http
GET /stats
```

**Response:**
```json
{
  "total_tasks": 5,
  "completed_tasks": 2,
  "pending_tasks": 3,
  "completion_rate": 40.0
}
```

---

## 🗄️ Database

### Schema

#### Tasks Table
```sql
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL UNIQUE,
  description TEXT,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Connect to Database

```bash
# Get PostgreSQL pod
POD=$(kubectl get pod -l app=postgres -o jsonpath='{.items[0].metadata.name}')

# Connect with psql
kubectl exec -it $POD -- psql -U devops_user -d devops_db

# Sample queries
SELECT * FROM tasks;
INSERT INTO tasks (title, description) VALUES ('New Task', 'Description');
UPDATE tasks SET completed = true WHERE id = 1;
DELETE FROM tasks WHERE id = 1;
```

---

## 🧪 Testing

### Backend Tests

```bash
cd final-project/backend

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=app
```

### Frontend Tests

```bash
cd final-project/frontend

# Install dependencies
npm install

# Run tests
npm test

# Build
npm run build
```

### Integration Tests

```bash
# 1. Deploy application
kubectl apply -k final-project/kubernetes/

# 2. Wait for readiness
kubectl wait --for=condition=ready pod -l app=backend --timeout=300s

# 3. Run tests
bash final-project/scripts/test.sh
```

---

## 🐛 Troubleshooting

### Pod won't start

```bash
# Check pod status
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

### Database connection failed

```bash
# Check PostgreSQL pod
kubectl get pod -l app=postgres

# Check logs
kubectl logs -l app=postgres

# Verify service
kubectl get svc postgres-service

# Test connection
kubectl run -it --rm debug --image=postgres:15-alpine --restart=Never -- \
  psql -h postgres-service -U devops_user -d devops_db -c "SELECT 1;"
```

### Backend/Frontend not responding

```bash
# Check service endpoints
kubectl get endpoints

# Test connectivity
kubectl run -it --rm curl --image=curlimages/curl --restart=Never -- \
  curl http://backend-service:8000/health

# Check port-forward
lsof -i :3000
lsof -i :8000
```

### Persistent volume not working

```bash
# Check PVC status
kubectl get pvc

# Check PV status
kubectl get pv

# Describe PVC
kubectl describe pvc postgres-pvc
```

---

## 📊 Monitoring

### View Metrics

```bash
# Pod resource usage
kubectl top pods

# Node resource usage
kubectl top nodes

# Watch deployments
kubectl get deployments -w

# Watch pods
kubectl get pods -w
```

### Check Logs

```bash
# Recent logs
kubectl logs -l app=backend --tail=50

# Follow logs
kubectl logs -f -l app=backend

# Previous logs (if crashed)
kubectl logs <pod-name> --previous
```

---

## 🤝 Contributing

### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make Changes**
   ```bash
   # Backend
   cd final-project/backend
   # ... make changes ...
   
   # Frontend
   cd final-project/frontend
   # ... make changes ...
   ```

3. **Test Locally**
   ```bash
   # Backend tests
   pytest tests/ -v
   
   # Frontend tests
   npm test
   ```

4. **Commit & Push**
   ```bash
   git add .
   git commit -m "feat: Add new feature"
   git push origin feature/your-feature
   ```

5. **Create Pull Request**
   - Open PR on GitHub
   - CI pipeline runs automatically
   - Request review

6. **Merge to Main**
   - After approval
   - Production deployment triggered

---

## 📝 License

MIT License - See LICENSE file

---

## �� Contact & Support

**Project Author**: Badr TAJINI  
**School**: ESIEE 2025  
**Email**: [your-email@example.com](mailto:your-email@example.com)  
**GitHub**: [@your-username](https://github.com/your-username)

---

## 🎯 Project Completion Status

- ✅ Backend API (FastAPI)
- ✅ Frontend UI (React)
- ✅ Database (PostgreSQL)
- ✅ Docker Images
- ✅ Kubernetes Manifests
- ✅ CI/CD Pipeline
- ✅ Documentation
- ✅ Testing
- ✅ Health Checks
- ✅ Security Scanning

**Overall Progress**: 100% ✅

---

**Last Updated**: December 6, 2024  
**Status**: Production Ready ✅

