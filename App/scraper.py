import logging
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

HOME_URL = "https://books.toscrape.com/"
TIMEOUT = 5
MAX_RETRIES = 2
RETRY_DELAY = 1
DEFAULT_TEXT = "Unknown"

REQUEST_COUNT = 0


def fetch_page(url):
    global REQUEST_COUNT

    for attempt in range(1, MAX_RETRIES + 2):
        REQUEST_COUNT += 1

        try:
            logging.info(f"Tentative {attempt}/{MAX_RETRIES + 1} : chargement de {url}")

            response = requests.get(url, timeout=TIMEOUT)

            if response.status_code == 200:
                return response.text

            logging.error(f"Erreur HTTP {response.status_code} pour l'URL : {url}")

            if response.status_code in [401, 403, 404]:
                return None

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
        logging.error(f"Erreur extraction note : {error}")
        return DEFAULT_TEXT


def extract_categories():
    html = fetch_page(HOME_URL)

    if html is None:
        logging.error("Impossible de récupérer la page d'accueil.")
        return []

    try:
        soup = BeautifulSoup(html, "html.parser")
        category_links = soup.select(".side_categories ul li ul li a")

        if not category_links:
            logging.error("Aucune catégorie trouvée dans le menu de gauche.")
            return []

        categories = []

        for link in category_links:
            category_name = get_text(link, "category_name")
            category_href = get_attribute(link, "href", "category_link", default=None)

            if not category_href:
                logging.warning(f"Lien manquant pour la catégorie : {category_name}")
                continue

            categories.append({
                "name": category_name,
                "url": urljoin(HOME_URL, category_href)
            })

        logging.info(f"{len(categories)} catégories récupérées")
        return categories

    except Exception as error:
        logging.exception(f"Erreur extraction catégories : {error}")
        return []


def extract_book(article, category_name, page_url):
    try:
        title_tag = article.select_one("h3 a")
        price_tag = article.find("p", class_="price_color")

        title = get_attribute(title_tag, "title", "title")
        price = get_text(price_tag, "price")
        rating = extract_rating(article)

        book_link = get_attribute(title_tag, "href", "book_link", default=None)
        source_url = urljoin(page_url, book_link) if book_link else DEFAULT_TEXT

        if source_url == DEFAULT_TEXT:
            logging.warning(f"URL du livre manquante pour : {title}")

        return {
            "title": title,
            "author": DEFAULT_TEXT,
            "price": price,
            "rating": rating,
            "category": category_name,
            "source_url": source_url
        }

    except Exception as error:
        logging.exception(f"Livre ignoré dans la catégorie {category_name} : {error}")
        return None


def get_next_page_url(soup, current_url):
    try:
        next_link = soup.select_one("li.next a")

        if next_link is None:
            return None

        href = get_attribute(next_link, "href", "next_page", default=None)

        if not href:
            logging.warning(f"Lien next invalide depuis : {current_url}")
            return None

        return urljoin(current_url, href)

    except Exception as error:
        logging.error(f"Erreur pagination depuis {current_url} : {error}")
        return None


def scrape_category(category):
    books = []
    category_name = category["name"]
    current_url = category["url"]
    page_number = 1

    while current_url:
        html = fetch_page(current_url)

        if html is None:
            logging.warning(f"Page ignorée pour la catégorie {category_name} : {current_url}")
            break

        try:
            soup = BeautifulSoup(html, "html.parser")
            articles = soup.find_all("article", class_="product_pod")

            if not articles:
                logging.warning(
                    f"Aucun livre trouvé pour {category_name}, page {page_number} : {current_url}"
                )
                break

            logging.info(
                f"Catégorie {category_name} - page {page_number} : {len(articles)} livres trouvés"
            )

            for article in articles:
                book = extract_book(article, category_name, current_url)

                if book is not None:
                    book["page_number"] = page_number
                    books.append(book)

            current_url = get_next_page_url(soup, current_url)
            page_number += 1

        except Exception as error:
            logging.exception(
                f"Erreur parsing catégorie {category_name}, page {page_number} : {error}"
            )
            break

    logging.info(f"Catégorie {category_name} terminée : {len(books)} livres récupérés")
    return books


def scrape_books():
    all_books = []
    categories = extract_categories()

    if not categories:
        logging.error("Scraping arrêté : aucune catégorie disponible.")
        return []

    for category in categories:
        books = scrape_category(category)
        all_books.extend(books)

    logging.info(f"Scraping terminé : {len(all_books)} livres récupérés")
    logging.info(f"Nombre total de requêtes HTTP : {REQUEST_COUNT}")

    return all_books


def get_request_count():
    return REQUEST_COUNT