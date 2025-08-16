import requests
from bs4 import BeautifulSoup
import time 

class BaseScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def get_pageContent(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
        
    def parse_html(self, html_content):
        if not html_content:
            return None
        return BeautifulSoup(html_content, 'lxml')
    
    def sleep(self, seconds = 1):
        time.sleep(seconds)

    
        