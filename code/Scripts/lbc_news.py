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

url = "https://www.lbc.co.uk/crime/"
BASE_URL = "https://www.lbc.co.uk"

def fetch_ibc_news(url):
    news_list = []
    footer_lnks = []
    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    

    news = soup.find_all('div', class_='article editorial promo long-form')
    # print(len(news))
    for new in news:
        headline = new.find('h3').text
        link = new.find('a')['href']
        if link == None:
            link = 'No link'
        else:

            link = BASE_URL + link
        img_url = new.find('img')['src']
        if img_url == None:
            img_url = 'No image'
        else:
            img_url = img_url

        print(img_url)
        print(headline)
        print(link)
        print('-------')

        driver.get(link)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        standfirst  = soup.find('p', class_ = "standfirst")
        if standfirst == None:
            standfirst = 'No standfirst'
        else:
            standfirst = standfirst.text

        content = soup.find_all('p', class_ = "paragraph-text")
        if content == None:
            content = 'No content'
        else:
                
            content = [c.text for c in content]
            content = ' '.join(content)
        print(standfirst)
        print(content)
        print('+++++++++++++++++++++++++++++++++')



        author = soup.find('p', class_ = "author-details__author")
        if author == None:
            author = 'No author'
        else:
                
            author = author.text if author else np.nan

        publish_date = soup.find('p', class_ = "publish_date")
        if publish_date == None:
            publish_date = 'No publish_date'
        else:
            publish_date = publish_date.text
            
        print(publish_date)
        print(author)

        news_list.append({
            'headline': headline,
            'link': link,
            'img_url': img_url,
            'standfirst': standfirst,
            'content': content,
            'author': author,
            'publish_date': publish_date
        })
        
    # Save to CSV
    df = pd.DataFrame(news_list)
    df.to_csv('lbc_news.csv', index=False)
    print("News data saved successfully.")


    return df

news_list = []
footer_lnks = []
driver.get(url)
time.sleep(2)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

footer_links  = soup.find_all('li', class_="footer-hot-links__item")
for link in footer_links:
    link = link.find('a')['href']
    if 'https' not in link:
        link = BASE_URL + link
    footer_lnks.append(link)
        
print(footer_lnks)
for link in footer_lnks:
    fetch_ibc_news(link)
    time.sleep(2)
    print('++++++++++++++')