# Utilisation d'une image légère de Node.js (pratique standard DevOps)
FROM node:18-alpine

# Dossier de travail dans le conteneur
WORKDIR /app

# Copie des fichiers de dépendances
COPY package*.json ./

# Installation des dépendances (sans les outils de test pour alléger l'image de prod)
RUN npm install --production

# Copie du reste du code
COPY . .

# L'API tourne sur le port 3000
EXPOSE 3000

# Commande de démarrage
CMD ["node", "server.js"]