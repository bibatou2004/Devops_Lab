FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY app.js .
COPY views ./views
EXPOSE 8080
CMD ["node", "app.js"]
