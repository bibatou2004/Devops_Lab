#!/bin/bash

set -e

echo "
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║  🚀 DEPLOYING TD6 MICROSERVICES 🚀                      ║
║                                                            ║
║     Backend + Frontend on Kubernetes                       ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Build images
echo ""
echo "📦 Building Docker images..."
echo "════════════════════════════════════════════════════════════"

echo "Building backend image..."
docker build -t sample-app-backend:latest "$SCRIPT_DIR/sample-app-backend"

echo "Building frontend image..."
docker build -t sample-app-frontend:latest "$SCRIPT_DIR/sample-app-frontend"

echo "✅ Images built"

# Deploy to Kubernetes
echo ""
echo "☸️  Deploying to Kubernetes..."
echo "════════════════════════════════════════════════════════════"

echo "Deploying backend..."
kubectl apply -f "$SCRIPT_DIR/sample-app-backend/sample-app-deployment.yml"
kubectl apply -f "$SCRIPT_DIR/sample-app-backend/sample-app-service.yml"

echo "Deploying frontend..."
kubectl apply -f "$SCRIPT_DIR/sample-app-frontend/sample-app-deployment.yml"
kubectl apply -f "$SCRIPT_DIR/sample-app-frontend/sample-app-service.yml"

echo "✅ Deployment files applied"

# Wait for deployments
echo ""
echo "⏳ Waiting for deployments..."
echo "════════════════════════════════════════════════════════════"

kubectl rollout status deployment/sample-app-backend-deployment
kubectl rollout status deployment/sample-app-frontend-deployment

echo "✅ Deployments ready"

# Show status
echo ""
echo "📊 Deployment Status"
echo "════════════════════════════════════════════════════════════"

echo ""
echo "Pods:"
kubectl get pods -l app=sample-app-backend-pods,app=sample-app-frontend-pods

echo ""
echo "Services:"
kubectl get svc -l app=sample-app-backend-pods,app=sample-app-frontend-pods

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ DEPLOYMENT COMPLETE! ✅                              ║"
echo "╚════════════════════════════════════════════════════════════╝"

echo ""
echo "🎊 Access frontend:"
echo "  kubectl port-forward svc/sample-app-frontend-loadbalancer 8080:80"
echo "  Then open: http://localhost:8080"

echo ""
echo "📊 Check status:"
echo "  kubectl get pods"
echo "  kubectl get svc"
echo "  kubectl logs -l app=sample-app-backend-pods -f"

echo ""
