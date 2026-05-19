# System Info Project

Ce projet permet d’obtenir un aperçu des informations principales de l’ordinateur utilisé ainsi que de l’environnement Python installé.

Le script affiche directement dans le terminal plusieurs informations système utiles pour le diagnostic et les tests d’environnement.

---

# Objectif du projet

Afficher rapidement des informations sur la machine utilisée :

* système d’exploitation
* nom de la machine
* version du système
* architecture de la machine
* version de Python

---

# Technologies utilisées

* Python
* module `platform`
* module `sys`

---

# Structure du projet

```bash
Session2/
│
├── src/
│   ├── main.py
│   ├── requirements.txt
│
├── data/
│   └── result.output
│
├── Dockerfile
├── docker-compose.yml
├── crontab.sh
│
└── README.md
```

---

# Fonctionnement du projet

Le projet est organisé autour d’une seule étape principale.

## 1️⃣ Affichage des informations système

Fichier : `main.py`

Le script utilise les librairies natives `sys` et `platform` pour récupérer les informations relatives à l’ordinateur.

Informations affichées :

* système d’exploitation
* nom de la machine
* version du système
* type de machine
* version de Python

---

# Code du projet

## main.py

```python
import platform
import sys


def system_info():
    print("System Information:")
    print(f"System: {platform.system()}")
    print(f"Node Name: {platform.node()}")
    print(f"Release: {platform.release()}")
    print(f"Machine: {platform.machine()}")
    print(f"Python Version: {sys.version}")
    print("------------------------------------")


if __name__ == "__main__":
    system_info()
```

---

# Exemple de sortie

```bash
System Information:
System: Linux
Node Name: ubuntu
Release: 24.04
Machine: x86_64
Python Version: 3.12.3
------------------------------------
```

---

# Installation

Aucune dépendance externe n’est nécessaire.

Vérifier simplement que Python est installé :

```bash
python3 --version
```

---

# Lancer le projet

Depuis le dossier `src` :

```bash
python3 main.py
```

Le script affichera automatiquement les informations système dans le terminal.

---

# Gestion des erreurs

Le projet utilise uniquement des modules natifs Python, ce qui limite fortement les risques d’erreurs.

Les informations sont récupérées directement depuis le système via les modules standards Python.

# Monitoring

Le projet utilise le module `logging` afin de suivre l’exécution du pipeline.

Les logs permettent de voir :

* le démarrage du pipeline
* les informations système récupérées
* le temps d’exécution
* la fin du pipeline

Les logs sont visibles dans Docker avec :

```bash
docker logs python-app