# Book Scraper Project

Ce projet consiste à construire un pipeline de données en Python permettant de scraper un site web, nettoyer les données récupérées et les sauvegarder dans un fichier CSV.

Le site utilisé est :

**Books to Scrape**

---

# Objectif du projet

Créer un pipeline ETL simple :

```text
Site web → Scraping → Nettoyage → Stockage CSV
```

Le pipeline peut être exécuté plusieurs fois et les nouvelles données sont ajoutées au fichier CSV existant.

---

# Technologies utilisées

* Python
* requests
* BeautifulSoup4
* pandas
* Docker
* Docker Compose
* cron
* logging

---

# Structure du projet

```text
Book Scraper Project/
│
├── App/
│   ├── scraper.py
│   ├── transform.py
│   └── main.py
│
├── data/
│   ├── books.csv
│   └── result.output
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── crontab.sh
└── README.md
```

---

# Fonctionnement du pipeline

Le pipeline est organisé en trois étapes.

## 1️⃣ Extraction des données

Fichier : `scraper.py`

Le script :

* parcourt les pages du catalogue
* récupère les livres
* extrait :
  * le titre
  * le prix
  * la note
  * la catégorie

---

## 2️⃣ Transformation des données

Fichier : `transform.py`

Les données sont nettoyées avec `pandas` :

* conversion du prix en nombre
* conversion des notes en valeurs numériques
* ajout de la date de scraping

Structure finale :

| date | title | category | price | rating |

---

## 3️⃣ Sauvegarde des données

Fichier : `main.py`

Les données sont sauvegardées dans :

```text
data/books.csv
```

Le fichier CSV est automatiquement créé et mis à jour à chaque exécution.

---

# Gestion des erreurs

Le pipeline gère plusieurs erreurs :

* site indisponible
* timeout réseau
* données manquantes
* erreur de conversion
* erreur de sauvegarde CSV

Les erreurs sont affichées dans les logs sans bloquer complètement le pipeline.

---

# Monitoring et logs

Le projet utilise le module `logging`.

Les logs permettent de suivre :

* le démarrage du pipeline
* le nombre de livres récupérés
* le temps d’exécution
* les erreurs éventuelles
* la fin du pipeline

Les logs sont sauvegardés dans :

```text
data/result.output
```

Ils sont également visibles avec Docker :

```bash
docker logs book_pipeline
```

---

# Dockerisation du projet

Le projet utilise Docker afin de :

* standardiser l’environnement
* automatiser l’exécution
* faciliter le déploiement

Le pipeline est automatisé avec `cron`.

---

# Installation

## Installer les dépendances Python

```bash
pip3 install -r requirements.txt
```

## Installer Docker

Installer :

* Docker Desktop
* Docker Compose

---

# Lancer le projet sans Docker

```bash
python3 App/main.py
```

---

# Lancer le projet avec Docker

## Construire l’image

```bash
docker compose build
```

## Lancer le conteneur

```bash
docker compose up
```

## Voir les logs

```bash
docker logs book_pipeline
```

## Arrêter le conteneur

```bash
docker compose down
```

---

# Exemple de résultat

```csv
date,title,category,price,rating
2026-03-31,A Light in the Attic,Poetry,51.77,3
2026-03-31,Tipping the Velvet,Historical Fiction,53.74,1
2026-03-31,Soumission,Fiction,50.10,1
```

---

# Bonnes pratiques

Le projet respecte plusieurs bonnes pratiques :

* séparation des responsabilités
* gestion des erreurs
* logs lisibles
* code structuré
* pipeline relançable

---

# Source des données

```text
https://books.toscrape.com/
```