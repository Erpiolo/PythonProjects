import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

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

url = 'http://books.toscrape.com/catalogue/page-1.html'
all_books = []

print("Iniciando scraping de 1 página...")

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

books_on_page = soup.find_all('article', class_='product_pod')
print(f"Scrapeando página 1 - {len(books_on_page)} libros encontrados.")

for book in books_on_page:
    book_data = parse_book(book)
    all_books.append(book_data)

df = pd.DataFrame(all_books)
df.to_csv('books.csv', index=False, encoding='utf-8')

print(f"\n¡Éxito! Se guardaron {len(all_books)} libros en 'books.csv'.")
