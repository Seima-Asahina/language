import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.yahoo.co.jp/'
res = requests.get(url)

soup = BeautifulSoup(res.text, "html.parser")

elems = soup.find_all(href=re.compile('https://news.yahoo.co.jp/pickup/'))

for elem in elems:
    pickup_links = [elem.attrs['href'] for elem in elems]
    print(pickup_links)
