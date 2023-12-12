import requests
from bs4 import BeautifulSoup
from collections import defaultdict


class Scrape:
    def __init__(self, url):
        self.headers = {
            'User-Agent': 'Mozilla/5.0(windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
            'Accept-Language': 'en-GB,en;q=0.5',  # English
            'Referer': 'https://google.com',
            'DNT': '1'  # 1-> True do not track
        }
        self.url = url
        self.session = requests.Session()
        self.response = self.session.get(url, headers=self.headers)
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.cookie = defaultdict(list)

    def savepage(self, page_name: str):
        with open(f'{page_name}.html', 'wb') as f:
            f.write(self.response.content)



            