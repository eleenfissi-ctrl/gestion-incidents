# 1. Image de base : Python 3.12 version légère
FROM python:3.12-slim

# Évite les fichiers .pyc et affiche les logs immédiatement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE=/data/incidents.db

# 2. Répertoire de travail dans le conteneur
WORKDIR /app

# 3. Copier d'abord requirements.txt puis 4. installer les dépendances
#    (Docker garde cette étape en cache tant que le fichier ne change pas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3 bis. Copier le code de l'application
COPY app/ ./app/

# Dossier où sera stockée la base SQLite (monté en volume par Compose)
RUN mkdir -p /data

# 5. Port de l'application
EXPOSE 5000

# 6. Commande de démarrage (gunicorn = serveur web adapté à la production)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
