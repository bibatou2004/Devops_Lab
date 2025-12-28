# Étape 1 : Build de l'application React
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# On définit l'URL par défaut pour le build (peut être écrasé par les args)
# Pour Minikube, on visera le NodePort du backend (voir étape suivante)
ENV REACT_APP_API_URL=http://localhost:30001
RUN npm run build

# Étape 2 : Serveur Web Nginx pour servir les fichiers statiques
FROM nginx:alpine
# Copie des fichiers buildés depuis l'étape 1 vers le dossier de Nginx
COPY --from=build /app/build /usr/share/nginx/html
# Exposition du port 80 (port standard web)
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]