from bs4 import BeautifulSoup
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# start a chrome browser session
driver = webdriver.Chrome()

driver.get('https://www.investopedia.com/')
time.sleep(2)
# get the page source
html = driver.page_source

# variable to store the links 
urls = []

soup = BeautifulSoup(html, 'html.parser')
# get all the links
links = soup.find_all('li', class_="comp terms-bar__item mntl-block")
for link in links:
    link = link.find('a')['href']
    # print(link)
    urls.append(link)

print(urls)


for url in urls:
    try:
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        data = []

        # get the title
        title = soup.find_all('a', class_='dictionary-top300-list__list mntl-text-link')
        for t in title:
            span_tag = t.find('span', class_="link__wrapper")
            if span_tag:
                title = span_tag.text.strip()
            if 'href' in t.attrs:
                link = t['href']
                # print(link)

            data.append({'title': title, 'link': link})
        # fetch the definition
        for link in data:
            if isinstance(link['link'], str):
                driver.get(link['link'])
                time.sleep(2)
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                main_title = soup.find('h1', class_="comp article-heading mntl-text-block")
                question = soup.find('span', class_="mntl-sc-block-heading__text")

                link['main_title'] = main_title.text if main_title else None
                link['question'] = question.text if question else None

        df = pd.DataFrame(data)
        df.to_csv('investopedia_data.csv')

        definition = soup.find_all('div', class_='comp article-body mntl-block')
        print(definition)

        print(data)

    except Exception as e:
        print(f"Error occurred for URL {url}: {e}")
        continue

driver.quit()
# comp article-heading mntl-text-block


