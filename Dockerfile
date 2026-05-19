# Image Python officielle
FROM python:3.9

# Dossier de travail dans le conteneur
WORKDIR /app

# Installer cron
RUN apt-get update && apt-get install -y cron

# Copier les dépendances
COPY requirements.txt .

# Installer les librairies Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . .

# Copier la configuration cron
COPY crontab.sh /etc/cron.d/book-pipeline-cron

# Donner les bonnes permissions
RUN chmod 0644 /etc/cron.d/book-pipeline-cron

# Installer la tâche cron
RUN crontab /etc/cron.d/book-pipeline-cron

# Lancer cron
CMD ["cron", "-f"]