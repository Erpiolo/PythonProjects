import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return None


def parse_book(book_article):
    title = book_article.find('h3').find('a')['title']

    price_text = book_article.find('p', class_='price_color').text
    price = float(re.search(r'[\d\.]+', price_text).group())

    rating_text = book_article.find('p', class_='star-rating')['class'][1]

    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    rating = rating_map.get(rating_text, 0)

    return {
        'Titulo': title,
        'Precio': price,
        'Rating': rating
    }


def main():
    base_url = 'http://books.toscrape.com/catalogue/'
    current_page = 1
    max_pages = 5
    all_books = []

    print(f"Iniciando scraping de {max_pages} páginas...")

    while current_page <= max_pages:
        url = f"{base_url}page-{current_page}.html"
        soup = get_soup(url)

        if not soup:
            print(f"No se pudo obtener la página {current_page}, deteniendo.")
            break

        books_on_page = soup.find_all('article', class_='product_pod')

        if not books_on_page:
            print("No se encontraron más libros. Deteniendo.")
            break

        print(f"Scrapeando página {current_page} - {len(books_on_page)} libros encontrados.")

        for book in books_on_page:
            book_data = parse_book(book)
            all_books.append(book_data)

        current_page += 1

    if not all_books:
        print("No se extrajo ningún dato.")
        return

    df = pd.DataFrame(all_books)
    df.to_csv('books.csv', index=False, encoding='utf-8')

    print(f"\n¡Éxito! Se guardaron {len(all_books)} libros en 'books.csv'.")


if __name__ == '__main__':
    main()