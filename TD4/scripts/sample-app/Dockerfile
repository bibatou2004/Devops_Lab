# Dockerfile
FROM node:21.7.3-alpine

WORKDIR /home/node/app

# Copier les fichiers de dépendances
COPY package.json .
COPY package-lock.json .

# Installer les dépendances (production uniquement)
RUN npm ci --only=production

# Copier le code
COPY *.js .

# Exposer le port
EXPOSE 8080

# Utilisateur non-root
USER node

# Démarrer l'application
CMD ["npm", "start"]
