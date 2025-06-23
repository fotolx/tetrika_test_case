import requests
import lxml.html
from time import sleep
import csv
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

def fetch_page(url, retries=3):
    for attempt in range(retries + 1):
        try:
            return requests.get(url).content
        except requests.exceptions.ConnectTimeout:
            if attempt < retries:
                sleep(10)
    return None

def parse_page(html):
    if not html:
        return {}, None
    tree = lxml.html.document_fromstring(html)
    animals = tree.xpath("//div[@class='mw-category-group']")
    beasts = {}
    for group in animals:
        items = group.text_content().replace(" ", "").split('\n')
        items.remove("") if '' in items else None
        letter = items[0]
        beasts[letter] = set(items[1:]) | beasts.get(letter, set())
    
    next_page = None
    nav_links = tree.xpath("//div[@id='mw-pages']/a")
    if nav_links and nav_links[-1].text_content() == 'Следующая страница':
        next_page = nav_links[-1].get('href')
    
    return beasts, next_page

def process_pages(base_url, start_url):
    beasts = {}
    url = start_url
    while url:
        html = fetch_page(base_url + url)
        if not html:
            return beasts
        new_beasts, next_page = parse_page(html)
        for letter, animals in new_beasts.items():
            beasts[letter] = beasts.get(letter, set()) | animals
        url = next_page
        sleep(2)
    return beasts

def save_to_csv(data, file):
    writer = csv.writer(file)
    for key in sorted(data):
        writer.writerow([key, len(data[key])])

class TestWikiAnimalsScraper(unittest.TestCase):
    
    @patch('requests.get')
    def test_fetch_page_success(self, mock_get):
        """Тест успешного получения страницы"""
        mock_response = MagicMock()
        mock_response.content = b'<html>content</html>'
        mock_get.return_value = mock_response
        
        content = fetch_page('https://valid.url')
        self.assertEqual(content, b'<html>content</html>')

    def test_parse_page_valid(self):
        """Тест парсинга валидного HTML"""
        html_content = """
        <div id="mw-pages">
        <div class="mw-category-group"><h3>A</h3>
            <ul><li><a>Animal1</a></li>
                <li><a>Animal2</a></li></ul>
        </div>
            <a href="/next_page">Следующая страница</a>
        </div>
        """
        animals, next_page = parse_page(html_content)
        self.assertEqual(animals, {'A': {'Animal1', 'Animal2'}})
        self.assertEqual(next_page, '/next_page')

    def test_parse_page_no_next_link(self):
        """Тест отсутствия следующей страницы"""
        html_content = """
        <div id="mw-pages">
        <div class="mw-category-group"><h3>B</h3>
            <ul><li>Bear</li></ul>
        </div>
            <a>Предыдущая страница</a>
        </div>
        """
        animals, next_page = parse_page(html_content)
        self.assertEqual(animals, {'B': {'Bear'}})
        self.assertIsNone(next_page)

    def test_parse_page_invalid_html(self):
        """Тест обработки поврежденного HTML"""
        html_content = "INVALID_HTML_CONTENT"
        animals, next_page = parse_page(html_content)
        self.assertEqual(animals, {})
        self.assertIsNone(next_page)

    @patch('__main__.fetch_page')
    def test_process_pages(self, mock_fetch):
        """Тест обработки нескольких страниц"""
        mock_fetch.side_effect = [
            # Страница 1
            """
            <div class="mw-category-group"><h3>A</h3>
                <ul><li>Ant</li></ul>
            </div>
            <div id="mw-pages">
                <a href="/page2">Следующая страница</a>
            </div>
            """,
            # Страница 2
            """
            <div class="mw-category-group"><h3>A</h3>
                <ul><li>Ape</li></ul>
            </div>
            <div id="mw-pages">
                <span>Конец</span>
            </div>
            """
        ]
        
        result = process_pages('https://start.url', '/start')
        self.assertEqual(result, {'A': {'Ant', 'Ape'}})

    def test_save_to_csv(self):
        """Тест записи данных в CSV"""
        data = {'A': ['Ant', 'Ape'], 'B': ['Bear']}
        with StringIO() as fake_file:
            save_to_csv(data, fake_file)
            fake_file.seek(0)
            reader = csv.reader(fake_file)
            rows = list(reader)
        
        self.assertEqual(rows, [['A', '2'], ['B', '1']])

    @patch('__main__.fetch_page')
    @patch('__main__.parse_page')
    def test_empty_response(self, mock_parse, mock_fetch):
        """Тест пустого ответа от сервера"""
        mock_fetch.return_value = ""
        mock_parse.return_value = {}, None
        result = process_pages('http://empty.url', '/empty')
        self.assertEqual(result, {})

if __name__ == '__main__':
    # Запуск тестов
    unittest.main(argv=[''], exit=False)

    # Основная логика
    print("Starting scraping...")
    base_url = 'https://ru.wikipedia.org'
    start_url = '/w/index.php?title=Категория:Животные_по_алфавиту'
    result = process_pages(base_url, start_url)
    print("Saving results...")
    with open('beasts.csv', 'w', newline='') as f:
        save_to_csv(result, f)
    print("Done! Results saved to beasts.csv")