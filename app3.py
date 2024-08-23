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
    sleep(1)

    
    #BeautihulSoupで解析
    url = elem_a.get_attribute("href")
    res = requests.get(url)
    res.encoding = 'shift-jis'
    soup = BeautifulSoup(res.text, "html.parser")

    #口コミ数を取得
    elem_review = soup.find('span', class_="reviewCount")
    reviews_text = elem_review.contents[1].text
    reviews =  int(reviews_text.replace('クチコミ', '').replace('件','').replace(',','').replace('口コミ','').strip())
    if reviews >= 20:
    #口コミページのURLを取得
        review_link1 = elem_review.contents[1].attrs['href']
        if review_link1.startswith("//"):
            review_link1 = "https:" + review_link1
        review_res = requests.get(review_link1)
        review_soup = BeautifulSoup(review_res.text,"html.parser")
        review_sentences = review_soup.find('p', class_="reviewCassette__comment")
        
            
        
    

    

    