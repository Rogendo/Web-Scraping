from bs4 import BeautifulSoup
import numpy as np
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# load the webdriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')

driver = webdriver.Chrome(options=options)

topics = ['academic-forum', 'afsdjn', 'journal', 'analysis', 'news-and-events', 'repository', 'video-content']

BASE_URL = 'https://www.afronomicslaw.org/index.php'
def scrape_afronomicslaw(topic, page=1):
# def scrape_afronomicslaw(page, topic):

    url = f'https://www.afronomicslaw.org/index.php/category/{topic}?page={page}'
    # url = 'https://www.afronomicslaw.org/index.php/category/academic-forum?page=1'

    data = []
    try:
        driver.get(url) 
        time.sleep(5)
        # get the page source
        html = driver.page_source
        # parse the page source
        soup = BeautifulSoup(html, 'html.parser')
        articles = soup.find_all('article', class_= 'node node--type-article node--promoted node--view-mode-teaser clearfix')
        if articles == None:
            articles = 'NaN'
        else:
            articles = articles
        
        for article in articles:
            title = article.find('span', class_="field field--name-title field--type-string field--label-hidden").text
            print(title)
            summary = article.find('div', class_='clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item').text
            print(summary)
            link = article.find('a')['href']
            link = BASE_URL + link
            print(link)
            tags = article.find('div','field field--name-field-tags field--type-entity-reference field--label-above clearfix').text
            print(tags)
            # simulate a click action on the link to access the full content
            driver.get(link)
            time.sleep(5)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            content = soup.find('div', class_='clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item').text
            print(content.text)


            data.append({
                'title': title,
                'tags': tags,
                'summary': summary,
                'content': content,
                'link': link
            })
        df = pd.DataFrame(data)
        df.to_csv('afronomicslaw.csv', index=False)

        return df

            
    
    except:
        print('Error')
    

for topic in topics:
    for i in range(1, 10):
        df = scrape_afronomicslaw(topic, i)
        df.to_csv('afronomicslaw.csv', index=False)
        time.sleep(5)
        print('Done')

               