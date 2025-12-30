# Image de base légère (Debian slim)
FROM python:3.9-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Installation des dépendances (en cache si inchangées)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste du code
COPY . .

# Port standard FastAPI
EXPOSE 8000

# Commande de lancement
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]