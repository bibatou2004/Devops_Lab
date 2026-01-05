#!/usr/bin/env bash
set -e

# Récupérer le nom et la version du package.json
name=$(npm pkg get name | tr -d '"')
version=$(npm pkg get version | tr -d '"')

echo "📦 Building Docker image: $name:$version"

# Construire l'image Docker
docker build \
  -t "$name:$version" \
  .

echo "✅ Image Docker built successfully: $name:$version"
