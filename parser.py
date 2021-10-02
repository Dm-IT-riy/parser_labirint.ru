import requests
from bs4 import BeautifulSoup
import csv
import json

def get_data():

    with open('books_data.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter = ';')

        writer.writerow(
            (
                'Название книги',
                'Автор книги',
                'Издатель',
                'Новая цена',
                'Старая цена',
                'Скидка (%)',
                'Статус'
            )
        )

    URL = 'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table'

    HEADERS = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.3.614 Yowser/2.5 Safari/537.36'
    }

    r = requests.get(url = URL, headers = HEADERS)
    soup = BeautifulSoup(r.text, 'lxml')

    pages_count = int(soup.find('div', class_ = 'pagination-numbers').find_all('a')[-1].text)
    
    books_data = []
    for page in range(1, pages_count + 1):
        url = f'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table&page={page}'

        r = requests.get(url = url, headers = HEADERS)
        soup = BeautifulSoup(r.text, 'lxml')

        books_items = soup.find('tbody', class_ = 'products-table__body').find_all('tr')

        for item in books_items:
            book_data = item.find_all('td')

            try:
                book_name = book_data[0].find('a').text.strip()
            except:
                book_name = 'Нет названия книги'

            try:
                book_author = book_data[1].find('a').text.strip()
            except:
                book_author = 'Нет автора'

            try:
                book_publishing = book_data[2].find_all('a')
                book_publishing = ': '.join([bp.text for bp in book_publishing])
            except:
                book_publishing = 'Нет издательства'

            try:
                book_new_price = book_data[3].find('div', class_ = 'price').find('span', class_ = 'price-val').find('span').text.strip().replace(' ', '')
            except:
                book_new_price = 'Нет новой стоимости'

            try:
                book_old_price = book_data[3].find('div', class_ = 'price').find('span', class_ = 'price-old').find('span').text.strip().replace(' ', '')
            except:
                book_old_price = 'Нет цены на товар'

            try:
                book_sale = round(((int(book_old_price) - int(book_new_price)) / int(book_old_price)) * 100)
            except:
                book_sale = 'Нет скидки'

            try:
                book_status = book_data[5].text.strip()
            except:
                book_status = 'Нет статуса'

            books_data.append(
                {
                    'book_name': book_name,
                    'book_author': book_author,
                    'book_publishing': book_publishing,
                    'book_new_price': book_new_price,
                    'book_old_price': book_old_price,
                    'book_sale': book_sale,
                    'book_status': book_status
                }
            )

            with open('books_data.csv', 'a', newline = '') as file:
                writer = csv.writer(file, delimiter = ';')

                writer.writerow(
                    (
                        book_name,
                        book_author,
                        book_publishing,
                        book_new_price,
                        book_old_price,
                        book_sale,
                        book_status
                    )
                )
        
        print(f'Обработана страница {page}/{pages_count}')

    with open('books_data.json', 'w', encoding = 'utf-8') as file:
        json.dump(books_data, file, indent = 4, ensure_ascii = False)

def main():
    get_data()

if __name__ == '__main__':
    main()
