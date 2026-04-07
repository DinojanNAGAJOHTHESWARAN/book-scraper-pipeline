import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
BOOK_BASE = "https://books.toscrape.com/catalogue/"

def scrape_books(pages=50):
    books = []

    for page in range(1, pages + 1):
        url = BASE_URL.format(page)
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status() 
        except requests.RequestException as e:
            print(f"[ERREUR] Impossible de charger la page {page}: {e}")
            continue 

        soup = BeautifulSoup(r.text, "html.parser")
        articles = soup.find_all("article", class_="product_pod")

        for book in articles:
            try:
                title = book.h3.a["title"]
                price = book.find("p", class_="price_color").text
                rating = book.p["class"][1]

                
                book_link = book.h3.a["href"]
                book_url = BOOK_BASE + book_link

                book_page = requests.get(book_url, timeout=5)
                book_page.raise_for_status()
                book_soup = BeautifulSoup(book_page.text, "html.parser")

                breadcrumb = book_soup.find("ul", class_="breadcrumb").find_all("li")
                category = breadcrumb[2].text.strip()
            except Exception as e:
                print(f"[ERREUR] Livre '{title if 'title' in locals() else 'inconnu'}' ignoré: {e}")
                continue 

            books.append({
                "title": title,
                "price": price,
                "rating": rating,
                "category": category
            })

    return books