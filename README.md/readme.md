⚽ Football News - Cloud Native DevOps Project

Auteur : Youcef GUEDIRI et Aibatou WANDAOGO Cours : DevOps & Data - ESIEE Paris Année : 2025-2026
 Présentation du Projet

Ce projet est une application micro-services complète déployée sur Kubernetes, permettant de suivre des scores de football en direct et de poster des commentaires analysés par un algorithme de sentiment (NLP).

Une démonstration complète du pipeline CI/CD et de la résilience du projet est disponible ici :

https://drive.google.com/drive/folders/1lNPzXDfRG5_bwutgPVgmhf6P-p0EjwpF?usp=drive_link



L'objectif pédagogique est de démontrer la maîtrise d'une chaîne DevOps complète : Conteneurisation, Orchestration Kubernetes, Persistance des données et Pipeline CI.
 Architecture Technique

Le projet repose sur une architecture 3-tiers découplée :

    Frontend (React + Nginx) :

        Hébergé dans un conteneur Nginx optimisé (Multi-stage build : Node.js pour le build, Nginx pour le run).

        Reverse Proxy : Nginx est configuré pour servir les fichiers statiques React ET rediriger les appels API (/api) vers le backend interne, résolvant ainsi les problèmes de CORS.

    Backend (FastAPI - Python) :

        API REST stateless exposée sur le port 8000.

        Implémente une logique de résilience (Retry Pattern) pour attendre la disponibilité de la base de données au démarrage.

        Sécurisé via JWT (Authentification) et analyse de sentiments basique (TextBlob/NLP).

    Base de Données (PostgreSQL) :

        Persistance assurée via PersistentVolumeClaim (PVC) Kubernetes.

        Données non volatiles : les utilisateurs et messages sont conservés même si le pod redémarre.

 Stack Technologique

    Local Cluster : Minikube

    Container Engine : Docker

    Orchestration : Kubernetes (Deployments, Services, Secrets, PVC)

    CI Pipeline : GitHub Actions (Tests unitaires + Build & Push Docker Hub)

    Backend : Python 3.9, FastAPI, Psycopg2

    Frontend : React 18, Nginx (Alpine)

 Guide d'Installation & Déploiement

Ce guide suppose que vous avez minikube, kubectl et docker installés sur votre machine.
1. Démarrage de l'environnement

Lancer Minikube avec le driver Docker :

minikube start --driver=docker

2. Déploiement sur Kubernetes

L'ordre d'application est important pour que les dépendances (Secrets, Volumes) soient prêtes avant les applications. Depuis la racine du projet :


# 1. Créer les Secrets (Mots de passe BDD & Clé API)
kubectl apply -f k8s/secrets.yaml

# 2. Créer le Volume Persistant pour la BDD (Stockage)
kubectl apply -f k8s/postgres.yaml

# 3. Déployer le Backend (API)
kubectl apply -f k8s/backend.yaml

# 4. Déployer le Frontend (Interface & Proxy)
kubectl apply -f k8s/frontend.yaml

# 5. Ou pour les appliquer tous en même temps direct
kubectl apply -f k8s

3. Vérification

Vérifiez que tous les pods sont en statut Running :

kubectl get pods

    Note : Il est normal si le pod backend redémarre 1 ou 2 fois (Status: CrashLoopBackOff) le temps que PostgreSQL s'initialise complètement. Le code gère ce cas automatiquement.

4. Accéder à l'application (Port-Forwarding)

Le projet tournant sur Minikube local, nous utilisons le Port-Forwarding pour accéder au service Frontend depuis la machine hôte.

Nous redirigeons le port local 3000 (standard React) vers le port 80 du conteneur Nginx.


# Redirige le port 3000 de votre machine vers le port 80 du cluster
kubectl port-forward service/frontend-service 3000:80

Ouvrez ensuite votre navigateur sur : http://localhost:3000
 Scénario de Démonstration (Validation)

Une fois l'application lancée, voici le scénario permettant de valider les objectifs du projet :

    Inscription & Auth : Créer un compte utilisateur. Le token JWT est généré et stocké.

    Live Score : Voir les scores s'afficher (données simulées par le backend).

    NLP & Data :

        Poster un message (ex: "Super match !").

        Le backend analyse le sentiment (Score positif) et le stocke en base.

    Test de Persistance (Crash Test) :

        Supprimer le pod de base de données : kubectl delete pod -l app=postgres

        Attendre que Kubernetes le recrée (Self-healing).

        Rafraîchir la page : Les données (utilisateurs/messages) sont toujours présentes grâce au PVC.

 CI/CD & Automatisation

Le projet inclut un pipeline GitHub Actions (.github/workflows/ci.yaml) automatisé :

    Tests Unitaires : Exécution de pytest sur le backend pour valider la logique avant tout build.

    Build & Push :

        Construction des images Docker optimisées.

        Push automatique sur le registre Docker Hub (noun25/foot-backend & noun25/foot-frontend).

    Note sur le CD (Continuous Deployment) : Le déploiement continu automatique (kubectl apply) n'est pas activé dans le pipeline car le cluster cible est Minikube (Local), inaccessible depuis les serveurs GitHub Actions. Dans un contexte Cloud (AKS/EKS), cette étape serait ajoutée.

 Justification des Choix Techniques

    Architecture Frontend (Nginx) : Utiliser Nginx dans le pod Frontend permet de servir les assets React performants tout en proxyfiant les requêtes API vers le service backend interne. Cela évite d'exposer inutilement le backend sur internet et gère proprement le CORS.

    Secrets Kubernetes : Les mots de passe ne sont jamais codés en dur dans les fichiers deployment.yaml mais injectés via des objets Secret (env: valueFrom: secretKeyRef), respectant les bonnes pratiques de sécurité.

    Database Init : L'initialisation des tables SQL est gérée au démarrage de l'application (dans main.py) pour simplifier le déploiement en une seule commande, sans nécessiter de conteneur de migration séparé pour ce projet scolaire.