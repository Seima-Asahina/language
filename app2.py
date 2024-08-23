import requests
from bs4 import BeautifulSoup
import re
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#ヘッドレスモード
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome('./chromedriver-win64/chromedriver',options=options)

#サイトの表示
driver.get('https://www.jalan.net/kankou/260000/')

for elem_a in driver.find_elements_by_xpath('//div[@class="item-info"]/p/a'):
    csvlist = []
    sleep(1)
    #BeautihulSoupで解析
    url = elem_a.get_attribute("href")
    res = requests.get(url)
    res.encoding = res.apparent_encoding  # 適切なエンコーディングを自動で設定
    soup = BeautifulSoup(res.text, "html.parser")

    #口コミ数を取得
    elem_review = soup.find('span', class_="reviewCount")
    reviews_text = elem_review.contents[1].text
    reviews =  int(reviews_text.replace('クチコミ', '').replace('件','').replace(',','').replace('口コミ','').strip())
    if reviews >= 20:
        review_link = elem_review.contents[1].attrs['href']
        review_link = "https:" + review_link
        driver.get(review_link)
        review_soup = BeautifulSoup(driver.page_source, "html.parser")

        review_title = review_soup.find('p', class_="detailTitle")
        print(review_title.text)