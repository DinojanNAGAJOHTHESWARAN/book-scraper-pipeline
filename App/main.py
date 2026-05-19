import logging
import time

from scraper import scrape_books
from transform import clean_data, save_csv


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    start_time = time.time()
    logging.info("Pipeline démarré")

    try:
        data = scrape_books()

        if not data:
            logging.warning("Aucune donnée récupérée. Pipeline arrêté proprement.")
            return

        logging.info(f"{len(data)} livres récupérés avant nettoyage")

        df = clean_data(data)

        logging.info(f"{len(df)} lignes prêtes à être sauvegardées")

        save_csv(df, "data/books.csv")

        execution_time = round(time.time() - start_time, 2)
        logging.info(f"Temps d'exécution total : {execution_time} secondes")
        logging.info("Pipeline terminé avec succès")

    except Exception as error:
        logging.exception(f"Erreur critique du pipeline : {error}")


if __name__ == "__main__":
    main()