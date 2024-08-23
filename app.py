import requests
from bs4 import BeautifulSoup
import re
import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#csvファイルを用意
#csv_date = datetime.datetime.today().strftime("%Y%m%d")
csv_file_name = 'jaran.csv'
f = open(csv_file_name, 'w', encoding='utf-8-sig', newline='')
writer = csv.writer(f, lineterminator='\n') 
csv_header = ["名前","スコア","口コミ"]
writer.writerow(csv_header)

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
    #口コミページのURLを取得
        review_link1 = elem_review.contents[1].attrs['href']
        if review_link1.startswith("//"):
            review_link1 = "https:" + review_link1
        driver.get(review_link1)
        review_soup = BeautifulSoup(driver.page_source, "html.parser")
        #タイトル
        review_title = review_soup.find('p', class_="detailTitle")
        csvlist.append(review_title.text)
        #スコア
        review_score = review_soup.find('span', class_="reviewPoint")
        csvlist.append(float(review_score.text))
        #口コミ
        review_sentences = review_soup.find_all('p', class_="reviewCassette__comment")
        for review_sentence in review_sentences:
            csvlist.append(review_sentence.text)

        #csvファイルに書き込み
        writer.writerow(csvlist)

f.close()