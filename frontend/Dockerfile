# Étape 1 : Build
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# CORRECTION : On utilise un chemin relatif. L'Ingress se chargera du routage.
ENV REACT_APP_API_URL=/api
RUN npm run build

# Étape 2 : Serveur Nginx
FROM nginx:alpine
# Ajout de la configuration personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]