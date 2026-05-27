FROM python:3.9

WORKDIR /app

# Installation de cron
RUN apt-get update && apt-get install -y cron

# Copie des dépendances
COPY App/requirements.txt .

# 🟢 NOUVEAU : Création d'un venv et installation des modules dedans
RUN python -m venv /app/venv
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copie de tout le projet
COPY . .

# Configuration et activation du Cron
COPY crontab.sh /etc/cron.d/book-pipeline-cron
RUN chmod 0644 /etc/cron.d/book-pipeline-cron
RUN crontab /etc/cron.d/book-pipeline-cron

# On lance Cron de manière standard au premier plan
CMD ["cron", "-f"]