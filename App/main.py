from scraper import scrape_books
from transform import clean_data, save_csv

def main():
    print("Scraping en cours...")
    try:
        data = scrape_books()
        if not data:
            print("[WARNING] Aucun livre récupéré.")
            return
    except Exception as e:
        print(f"[ERREUR] Scraping échoué: {e}")
        return

    print("Transformation des données...")
    try:
        df = clean_data(data)
    except Exception as e:
        print(f"[ERREUR] Transformation échouée: {e}")
        return

    print("Sauvegarde CSV...")
    try:
        save_csv(df, "data/books.csv")
    except Exception as e:
        print(f"[ERREUR] Sauvegarde échouée: {e}")
        return

    print("Pipeline terminé ✔")

if __name__ == "__main__":
    main()