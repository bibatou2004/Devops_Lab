# Architecture Documentation

## System Overview

This project implements a complete DevOps pipeline with:
- **Frontend**: React single-page application
- **Backend**: FastAPI REST API
- **Database**: PostgreSQL relational database
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions

## Component Architecture

### Frontend Component

```
React Application (Port 3000)
├── Components
│   ├── Task List
│   ├── Task Form
│   └── Statistics Dashboard
├── State Management
│   └── React Hooks
└── API Integration
    └── Fetch API to Backend
```

**Technology**: 
- React 18.2
- ES6+ JavaScript
- CSS3
- Responsive Design

### Backend Component

```
FastAPI Application (Port 8000)
├── Routes
│   ├── /health
│   ├── /tasks (CRUD)
│   └── /stats
├── Business Logic
│   └── CRUD Operations
├── Database Layer
│   └── SQLAlchemy ORM
└── Security
    ├── CORS
    └── Validation
```

**Technology**:
- FastAPI 0.104
- Python 3.11
- SQLAlchemy 2.0
- Pydantic validation

### Database Component

```
PostgreSQL Database (Port 5432)
├── Tasks Table
│   ├── id (PK)
│   ├── title (UNIQUE)
│   ├── description
│   ├── completed (BOOL)
│   ├── created_at (TS)
│   └── updated_at (TS)
└── Indexes
    └── idx_tasks_title
```

**Technology**:
- PostgreSQL 15
- Persistent Volumes
- 5Gi Storage

## Deployment Architecture

### Kubernetes Deployment

```yaml
Namespace: default

Services:
├── frontend-service (LoadBalancer)
│   ├── Type: LoadBalancer
│   ├── Port: 80
│   └── Target: 3000
├── backend-service (ClusterIP)
│   ├── Type: ClusterIP
│   ├── Port: 8000
│   └── Target: 8000
└── postgres-service (ClusterIP)
    ├── Type: ClusterIP
    ├── Port: 5432
    └── Target: 5432

Deployments:
├── frontend-deployment (3 replicas)
├── backend-deployment (3 replicas)
└── postgres-deployment (1 replica)

Storage:
└── postgres-pvc (5Gi)

ConfigMaps:
├── frontend-config
├── backend-config
└── postgres-config

Secrets:
├── backend-secret
└── postgres-secret
```

## CI/CD Pipeline Architecture

```
GitHub Repository
├── Main Branch
│   ├── Triggers: CI/CD
│   ├── Deployments: Production
│   └── Environment: prod
└── Develop Branch
    ├── Triggers: CI/CD
    ├── Deployments: Staging
    └── Environment: staging

CI/CD Pipeline:
├── Stage 1: Code Checkout
├── Stage 2: Lint & Test (Backend)
├── Stage 3: Build & Test (Frontend)
├── Stage 4: Security Scanning
├── Stage 5: Build Docker Images
├── Stage 6: Push to Registry
├── Stage 7: Deploy to Staging (develop)
└── Stage 8: Deploy to Production (main)
```

## Network Architecture

```
Internet
├── (LoadBalancer 0.0.0.0:80)
│
└── Kubernetes Cluster
    ├── Frontend Pod 1 (3000)
    ├── Frontend Pod 2 (3000)
    ├── Frontend Pod 3 (3000)
    │   └── → Backend Service (Port 8000)
    │       ├── Backend Pod 1 (8000)
    │       ├── Backend Pod 2 (8000)
    │       └── Backend Pod 3 (8000)
    │           └── → PostgreSQL Service (Port 5432)
    │               └── PostgreSQL Pod (5432)
    │                   └── Persistent Volume
    │
    └── kube-dns (Service Discovery)
```

## Data Flow

### Create Task Flow

```
1. User Input
   React Component → Form

2. API Request
   Frontend → POST /tasks (Backend)

3. Validation
   Pydantic Schema

4. Database Operation
   ORM → INSERT INTO tasks

5. Response
   Backend → JSON Response

6. UI Update
   React State Update
```

### Update Task Flow

```
1. User Action
   React Component → Checkbox/Button

2. API Request
   Frontend → PUT /tasks/{id} (Backend)

3. Validation & Update
   ORM → UPDATE tasks

4. Database Commit
   Transaction completed

5. Response
   Backend → Updated Task

6. UI Refresh
   React State Update
```

## Scalability Architecture

### Horizontal Scaling

```
Load Balancer
├── Frontend Pod (3 replicas → N replicas)
├── Backend Pod (3 replicas → N replicas)
└── Database (1 replica)
    └── Can add Read Replicas
        ├── Replica 1 (Read-Only)
        └── Replica 2 (Read-Only)
```

### Resource Management

```
Frontend:
├── CPU Request: 100m
├── CPU Limit: 300m
├── Memory Request: 128Mi
└── Memory Limit: 256Mi

Backend:
├── CPU Request: 250m
├── CPU Limit: 500m
├── Memory Request: 256Mi
└── Memory Limit: 512Mi

Database:
├── CPU Request: 250m
├── CPU Limit: 500m
├── Memory Request: 256Mi
└── Memory Limit: 512Mi
```

## Security Architecture

```
Security Layers:
1. Container Security
   ├── Distroless images
   ├── Read-only root filesystem
   └── No root user

2. Pod Security
   ├── Network Policies
   ├── RBAC (Role-Based Access Control)
   └── Pod Security Policies

3. Secret Management
   ├── Encrypted secrets
   ├── ConfigMaps for non-sensitive data
   └── No hardcoded credentials

4. Image Security
   ├── Trivy scanning
   ├── Base image updates
   └── Security fixes applied

5. Network Security
   ├── TLS/HTTPS (Production)
   ├── Service-to-service auth
   └── Ingress security
```

## Persistence Architecture

```
PostgreSQL Persistent Storage
├── PersistentVolumeClaim (5Gi)
├── Storage Class: default
└── Access Mode: ReadWriteOnce

Data Backup Strategy:
├── Volume Snapshots
├── Database Dumps
│   └── pg_dump periodic backups
└── Replication
    └── Read replicas in production
```

---

**Last Updated**: December 2024
