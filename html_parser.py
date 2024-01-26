import requests
from bs4 import BeautifulSoup

class HTMLParser:
    @staticmethod
    def fetch_text_from_paragraphs(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                paragraphs = soup.find_all('p')
                all_text = ' '.join([para.get_text(strip=True) for para in paragraphs])
                return all_text
        except requests.RequestException:
            return None