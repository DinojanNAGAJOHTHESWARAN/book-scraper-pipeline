import logging
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
BOOK_BASE_URL = "https://books.toscrape.com/catalogue/"
TIMEOUT = 5
MAX_RETRIES = 2
RETRY_DELAY = 1
DEFAULT_TEXT = "Unknown"


def fetch_page(url):
    for attempt in range(1, MAX_RETRIES + 2):
        try:
            logging.info(f"Tentative {attempt}/{MAX_RETRIES + 1} : chargement de {url}")

            response = requests.get(url, timeout=TIMEOUT)

            if response.status_code == 200:
                return response.text

            logging.error(
                f"Erreur HTTP {response.status_code} pour l'URL : {url}"
            )

            if response.status_code == 404:
                logging.warning(f"Page inexistante : {url}")
                return None

            if response.status_code in [401, 403]:
                logging.error(f"Accès refusé pour l'URL : {url}")
                return None

            if response.status_code >= 500:
                logging.warning(f"Erreur serveur temporaire possible : {url}")

        except requests.exceptions.Timeout:
            logging.error(f"Timeout après {TIMEOUT}s pour l'URL : {url}")

        except requests.exceptions.ConnectionError:
            logging.error(f"Erreur de connexion pour l'URL : {url}")

        except requests.exceptions.TooManyRedirects:
            logging.error(f"Trop de redirections pour l'URL : {url}")
            return None

        except requests.exceptions.RequestException as error:
            logging.error(f"Erreur réseau pour l'URL {url} : {error}")

        if attempt <= MAX_RETRIES:
            logging.info(f"Nouvelle tentative dans {RETRY_DELAY} seconde(s)")
            time.sleep(RETRY_DELAY)

    logging.error(f"Échec définitif après {MAX_RETRIES + 1} tentatives : {url}")
    return None


def get_text(element, field_name, default=DEFAULT_TEXT):
    if element is None:
        logging.warning(f"Champ manquant : {field_name}")
        return default

    text = element.get_text(strip=True)

    if not text:
        logging.warning(f"Champ vide : {field_name}")
        return default

    return text


def get_attribute(element, attribute, field_name, default=DEFAULT_TEXT):
    if element is None:
        logging.warning(f"Balise manquante pour le champ : {field_name}")
        return default

    value = element.get(attribute)

    if not value:
        logging.warning(f"Attribut '{attribute}' manquant pour : {field_name}")
        return default

    return value.strip()


def extract_rating(article):
    try:
        rating_tag = article.find("p")
        classes = rating_tag.get("class", []) if rating_tag else []

        valid_ratings = ["One", "Two", "Three", "Four", "Five"]

        for rating in classes:
            if rating in valid_ratings:
                return rating

        logging.warning(f"Format de note inconnu : {classes}")
        return DEFAULT_TEXT

    except Exception as error:
        logging.error(f"Erreur lors de l'extraction de la note : {error}")
        return DEFAULT_TEXT


def extract_category(book_url):
    html = fetch_page(book_url)

    if html is None:
        logging.warning(f"Catégorie non récupérée, URL produit inaccessible : {book_url}")
        return DEFAULT_TEXT

    try:
        soup = BeautifulSoup(html, "html.parser")
        breadcrumb = soup.find("ul", class_="breadcrumb")

        if breadcrumb is None:
            logging.warning(f"Breadcrumb introuvable pour : {book_url}")
            return DEFAULT_TEXT

        items = breadcrumb.find_all("li")

        if len(items) < 3:
            logging.warning(f"Catégorie absente ou breadcrumb incomplet pour : {book_url}")
            return DEFAULT_TEXT

        category = get_text(items[2], "category")

        if category == DEFAULT_TEXT:
            logging.warning(f"Nom de catégorie invalide pour : {book_url}")

        return category

    except Exception as error:
        logging.error(f"Erreur parsing catégorie pour {book_url} : {error}")
        return DEFAULT_TEXT


def extract_author(book_url):
    logging.info(f"Auteur non disponible sur Books to Scrape : {book_url}")
    return DEFAULT_TEXT


def extract_book(article, page_number):
    try:
        title_tag = article.select_one("h3 a")
        price_tag = article.find("p", class_="price_color")

        title = get_attribute(title_tag, "title", "title")
        price = get_text(price_tag, "price")
        rating = extract_rating(article)

        book_link = get_attribute(title_tag, "href", "book_link", default=None)

        if book_link:
            book_url = urljoin(BOOK_BASE_URL, book_link)
        else:
            logging.warning(f"Lien produit manquant pour le livre : {title}")
            book_url = DEFAULT_TEXT

        if book_url != DEFAULT_TEXT:
            category = extract_category(book_url)
            author = extract_author(book_url)
        else:
            category = DEFAULT_TEXT
            author = DEFAULT_TEXT

        return {
            "title": title,
            "author": author,
            "price": price,
            "rating": rating,
            "category": category,
            "source_url": book_url,
            "page_number": page_number
        }

    except Exception as error:
        logging.exception(f"Livre ignoré sur la page {page_number} : {error}")
        return None


def scrape_books(max_pages=50):
    books = []
    pages_without_books = 0

    for page in range(1, max_pages + 1):
        url = BASE_URL.format(page)
        html = fetch_page(url)

        if html is None:
            logging.warning(f"Page {page} ignorée : {url}")
            pages_without_books += 1

            if pages_without_books >= 2:
                logging.warning("Arrêt pagination : plusieurs pages consécutives invalides.")
                break

            continue

        try:
            soup = BeautifulSoup(html, "html.parser")
            articles = soup.find_all("article", class_="product_pod")

            if not articles:
                logging.warning(f"Aucun livre trouvé sur la page {page} : {url}")
                pages_without_books += 1

                if pages_without_books >= 2:
                    logging.warning("Arrêt pagination : plusieurs pages consécutives sans livres.")
                    break

                continue

            pages_without_books = 0
            logging.info(f"Page {page} : {len(articles)} livres trouvés")

            for article in articles:
                book = extract_book(article, page)

                if book is not None:
                    books.append(book)

        except Exception as error:
            logging.exception(f"Erreur parsing page {page} : {error}")
            continue

    logging.info(f"Scraping terminé : {len(books)} livres récupérés")
    return books