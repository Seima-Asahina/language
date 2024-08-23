for elem_a in driver.find_elements_by_xpath('//div[@class="item-info"]/p/a'):
    csvlist = []
    sleep(1)
    try:
        # BeautihulSoupで解析
        url = elem_a.get_attribute("href")
        res = requests.get(url)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, "html.parser")

        # 口コミ数を取得
        elem_review = soup.find('span', class_="reviewCount")
        reviews_text = elem_review.contents[1].text
        reviews = int(reviews_text.replace('クチコミ', '').replace('件','').replace(',','').replace('口コミ','').strip())
        if reviews >= 20:
            # 口コミページのURLを取得
            review_link1 = elem_review.contents[1].attrs['href']
            if review_link1.startswith("//"):
                review_link1 = "https:" + review_link1
            driver.get(review_link1)
            review_soup = BeautifulSoup(driver.page_source, "html.parser")

            # タイトル
            review_title = review_soup.find('p', class_="detailTitle")
            csvlist.append(review_title.text)

            # スコア
            review_score = review_soup.find('span', class_="reviewPoint")
            csvlist.append(float(review_score.text))

            # 口コミ
            review_sentences = review_soup.find_all('p', class_="reviewCassette__comment")
            for review_sentence in review_sentences:
                csvlist.append(review_sentence.text)

            review_link2 = review_soup.find('a', class_="next")
            if review_link2:
                review_link2 = review_link2.attrs['href']
                if review_link2.startswith("//"):
                    review_link2 = "https:" + review_link2

                print(f"Navigating to: {review_link2}")
                driver.get(review_link2)

                review_soup2 = BeautifulSoup(driver.page_source, "html.parser")
                review_sentences = review_soup2.find_all('p', class_="reviewCassette__comment")

            # csvファイルに書き込み
            writer.writerow(csvlist)

    except selenium.common.exceptions.StaleElementReferenceException:
        print("StaleElementReferenceException occurred, retrying...")
        continue  # スキップして次の要素に進む

    except Exception as e:
        print(f"An error occurred: {e}")
