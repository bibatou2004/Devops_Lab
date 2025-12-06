#!/bin/bash

echo "
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║  🧹 CLEANING UP TD6 RESOURCES 🧹                       ║
║                                                            ║
║     Removing deployments and services                      ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "Deleting backend deployment..."
kubectl delete deployment sample-app-backend-deployment --ignore-not-found

echo "Deleting backend service..."
kubectl delete svc sample-app-backend-service --ignore-not-found

echo "Deleting frontend deployment..."
kubectl delete deployment sample-app-frontend-deployment --ignore-not-found

echo "Deleting frontend service..."
kubectl delete svc sample-app-frontend-loadbalancer --ignore-not-found

echo ""
echo "✅ Cleanup complete!"

echo ""
echo "Remaining resources:"
kubectl get pods,svc

echo ""
