from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup


# Set up Selenium with headless Chrome
chrome_options = Options()

chrome_options.headless = True
driver = webdriver.Chrome(options=chrome_options)

import requests


def get_climate_articles(year, page):
    """
    This function scrapes the Nature Climate Change website for articles published in a given year and page.
    
    Parameters:
    year: int, the year of publication
    page: int, the page number to scrape
    
    return: DataFrame, a DataFrame containing the title, authors, and summary of the articles on the page

    """

    f_url = f"https://www.nature.com/nclimate/articles?searchType=journalSearch&sort=PubDate&type=article&year={year}&page={page}"
    driver.get(f_url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all("div", class_="u-full-height")
    article_list = []
    for article in articles:
        title = article.find("h3", class_="c-card__title").text
        link = article.find("a", class_="c-card__link u-link-inherit")["href"]
        link = f"https://www.nature.com{link}"

        authors = article.find_all("ul", class_="c-author-list c-author-list--compact c-author-list--truncated")
        authors = [author.text for author in authors]
        authors_tags = article.find_all("ul", class_="c-author-list c-author-list--compact c-author-list--truncated")
        authors = []
        for author_tag in authors_tags:
            author_names = author_tag.find_all("li")
            authors.extend([author_name.text.strip() for author_name in author_names])
        if not authors:
            authors = ["No authors"]
        summary = article.find("div", class_="c-card__summary").text
        # abstract  
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        abstract = soup.find("div", class_="c-article-section__content")
        if abstract:
            abstract = abstract.text
        else:
            abstract = "No content"
        reference = soup.find("p", class_="c-article-references__text")
        
        content = soup.find("div", class_="main-content")
        if content:
            content = content.text
        else:
            content = "No content"

        if reference:
            reference = reference.text
        else:
            reference = "No content"

        article_list.append({"title": title, "authors": authors, "summary": summary, "link": link, "abstract": abstract, "content":content, "reference": reference})
    return pd.DataFrame(article_list)

# df = get_climate_articles(2021,1)
# df.head()


all_data = []

pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
years = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]

for page in pages:
    for year in years:
        df = get_climate_articles(year, page)
        all_data.append(df)
        print(f"Extracted data for year {year}, page {page}")

# Concatenate all data into a single DataFrame
final_df = pd.concat(all_data, ignore_index=True)


# Save the concatenated DataFrame to a single CSV file
final_df.to_csv("all_climate_articles.csv", index=False)
print("Saved all_climate_articles.csv")
