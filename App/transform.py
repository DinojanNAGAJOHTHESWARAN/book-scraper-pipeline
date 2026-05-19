import logging
import os
from datetime import datetime

import pandas as pd

DEFAULT_TEXT = "Unknown"


def clean_text(value, field_name):
    try:
        if value is None:
            logging.warning(f"{field_name} manquant")
            return DEFAULT_TEXT

        value = str(value).strip()

        if not value or value.lower() in ["nan", "none", "null"]:
            logging.warning(f"{field_name} vide ou invalide")
            return DEFAULT_TEXT

        return value

    except Exception as error:
        logging.error(f"Erreur nettoyage texte pour {field_name} : {error}")
        return DEFAULT_TEXT


def clean_price(price):
    try:
        if price is None:
            logging.warning("Prix manquant")
            return pd.NA

        price = str(price).strip()
        cleaned_price = "".join(char for char in price if char.isdigit() or char == ".")

        if not cleaned_price:
            logging.warning(f"Prix invalide : {price}")
            return pd.NA

        return float(cleaned_price)

    except ValueError:
        logging.error(f"Format de prix non convertible : {price}")
        return pd.NA

    except Exception as error:
        logging.error(f"Erreur inattendue sur le prix '{price}' : {error}")
        return pd.NA


def clean_rating(rating):
    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    try:
        rating = clean_text(rating, "rating")

        if rating not in rating_map:
            logging.warning(f"Note inconnue : {rating}")
            return 0

        return rating_map[rating]

    except Exception as error:
        logging.error(f"Erreur nettoyage note : {error}")
        return 0


def clean_data(data):
    if not data:
        raise ValueError("Aucune donnée à nettoyer.")

    df = pd.DataFrame(data)

    expected_columns = [
        "title",
        "author",
        "price",
        "rating",
        "category",
        "source_url",
        "page_number"
    ]

    for column in expected_columns:
        if column not in df.columns:
            logging.warning(f"Colonne manquante ajoutée : {column}")
            df[column] = DEFAULT_TEXT

    df["title"] = df["title"].apply(lambda value: clean_text(value, "title"))
    df["author"] = df["author"].apply(lambda value: clean_text(value, "author"))
    df["category"] = df["category"].apply(lambda value: clean_text(value, "category"))
    df["source_url"] = df["source_url"].apply(lambda value: clean_text(value, "source_url"))
    df["price"] = df["price"].apply(clean_price)
    df["rating"] = df["rating"].apply(clean_rating)
    df["date"] = datetime.today().strftime("%Y-%m-%d")

    df = df[
        [
            "date",
            "title",
            "author",
            "category",
            "price",
            "rating",
            "source_url",
            "page_number"
        ]
    ]

    logging.info(f"Transformation terminée : {len(df)} lignes nettoyées")
    return df


def save_csv(df, path):
    if df.empty:
        raise ValueError("Le DataFrame est vide, sauvegarde annulée.")

    try:
        directory = os.path.dirname(path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        file_exists = os.path.exists(path)

        df.to_csv(
            path,
            index=False,
            mode="a",
            header=not file_exists,
            encoding="utf-8"
        )

        logging.info(f"CSV sauvegardé avec succès : {path}")

    except PermissionError:
        logging.exception(f"Permission refusée lors de la sauvegarde : {path}")
        raise

    except OSError as error:
        logging.exception(f"Erreur système lors de la sauvegarde CSV : {error}")
        raise