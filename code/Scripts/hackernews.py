import pandas as pd
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from docx import Document
import uuid
import re
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup

def setup_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

driver = setup_driver()

url = 'https://thehackernews.com/'
data = []
driver = setup_driver()

def get_page(url):
    
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all("div", class_='clear home-post-box cf')
    for article in articles:
        title = article.find("h2", class_='home-title')
        # print(title.text)
        title = title.text

        link = soup.find("a", class_='story-link')['href']
        # print(link)
        content, author = get_article(link)

        data.append({
            'title': title,
            'link': link,
            'content': content,
            'author': author
        })
    df = pd.DataFrame(data)
    df.to_csv('thehackernews_pg2.csv')
    return data


def get_article(url):
    driver.get(url)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    article = soup.find("div", class_='articlebody clear cf')
    # print(article.text)
    article = article.text

    author = soup.find("span", class_='p-author')
    author = author.text

    return article, author

if __name__ == '__main__':

    get_page(url)