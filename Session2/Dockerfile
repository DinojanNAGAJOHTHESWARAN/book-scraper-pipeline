# Image Python officielle
FROM python:3.9-slim

# Dossier de travail dans le conteneur
WORKDIR /app

RUN apt-get update && apt-get install -y cron

COPY src/ /app/

COPY crontab.sh /etc/cron.d/data-pipeline-cron

RUN chmod +x /etc/cron.d/data-pipeline-cron
RUN crontab /etc/cron.d/data-pipeline-cron

RUN pip install -r requirements.txt

CMD ["cron", "-f"]