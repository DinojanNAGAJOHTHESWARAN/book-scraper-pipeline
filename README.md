# Book Scraper Project

Ce projet consiste à construire un **petit pipeline de données en Python** qui scrape un site web, nettoie les données et les stocke dans un fichier CSV exploitable.

Le site utilisé est :

Books to Scrape

Ce site est spécialement conçu pour pratiquer le **web scraping**.

---

# Objectif du projet

Créer un pipeline simple :

```
Site web → Scraping → Nettoyage des données → Stockage CSV
```

Le pipeline peut être exécuté **plusieurs fois**, et les nouvelles données sont **ajoutées au fichier existant**.

---

# Technologies utilisées

* Python
* requests (requêtes HTTP)
* BeautifulSoup (parsing HTML)
* pandas (transformation des données)

---

# Structure du projet

```
Data Pipelines/
│
├── App/
│   ├── scraper.py
│   ├── transform.py
│   └── main.py
│
├── data/
│   └── books.csv
│
└── README.md
```

---

# Fonctionnement du pipeline

Le projet est organisé en **trois étapes principales**.

## 1️⃣ Scraping (Extract)

Fichier : `scraper.py`

Le script :

* parcourt les pages du catalogue
* récupère les informations principales des livres
* visite la page de chaque livre pour extraire la catégorie

Données récupérées :

* titre
* prix
* note
* catégorie

Les erreurs réseau ou de parsing sont gérées avec `try/except` pour éviter de bloquer le pipeline.

---

## 2️⃣ Transformation des données (Transform)

Fichier : `transform.py`

Les données sont nettoyées avec **pandas** :

* conversion du prix en nombre (`float`)
* transformation des notes texte (`One`, `Two`, etc.) en valeur numérique
* ajout de la **date de scraping**

Structure finale :

| date | title | category | price | rating |

---

## 3️⃣ Sauvegarde des données (Load)

Les données sont sauvegardées dans :

```
data/books.csv
```

Le script :

* crée le dossier `data` si nécessaire
* ajoute les nouvelles lignes au fichier existant
* évite d’écraser les données précédentes

Cela permet de **lancer le pipeline plusieurs fois**.

---

# Installation

Installer les dépendances :

```bash
pip3 install requests beautifulsoup4 pandas
```

---

# Lancer le projet

Depuis le dossier `App` :

```bash
python3 main.py
```

Le script va :

1. scraper les données
2. nettoyer les données
3. ajouter les résultats dans `data/books.csv`

---

# Exemple de résultat

```
date,title,category,price,rating
31-03-2026,A Light in the Attic,Poetry,51.77,3
31-03-2026,Tipping the Velvet,Historical Fiction,53.74,1
31-03-2026,Soumission,Fiction,50.10,1
```

---

# Gestion des erreurs

Le pipeline gère plusieurs types d'erreurs :

* site indisponible
* page manquante
* problème de format de données
* erreur de sauvegarde CSV

Les erreurs sont affichées mais **le pipeline continue de fonctionner**.
