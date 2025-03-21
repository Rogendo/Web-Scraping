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

def scrape_poems():
    """
    This function scrapes poems from the poetry foundation website
    and exports the data to a csv file

    Returns:
    df: a dataframe of the scraped data
    """
    BASE_URL = "https://www.poetryfoundation.org"
    urls = [
        "https://www.poetryfoundation.org/categories/winter",
        "https://www.poetryfoundation.org/categories/love",
        "https://www.poetryfoundation.org/categories/youth",
        "https://www.poetryfoundation.org/categories/relationships",
        "https://www.poetryfoundation.org/categories/travels-journeys",
        "https://www.poetryfoundation.org/categories/history-politics",
    ]

    data = []  # to store the data

    for url in urls:
        # get the page
        driver.get(url)
        time.sleep(2)
        # get the page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        poems = soup.find_all('li', class_="col-span-full pt-6")
        for p in poems:
            title = p.find('h3').text
            author = p.find('div', class_="type-kappa text-gray-600")
            if author:
                author = author.text
            else:
                author = None
            summary = p.find('div', class_="rich-text line-clamp-[var(--line-clamp)]")
            if summary:
                summary = summary.text
            else:
                summary = None

            link = p.find('a')['href']
            # Being the link is a short link, we need to add the base url to it to access the entire poem
            link = BASE_URL + link

            # simulate a click action to click the link to access the entire poem in the next page!
            driver.get(link)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            poem = soup.find('article', class_="mb-6 flex flex-col gap-12 md:mb-0")  # get the poem
            if poem:
                poem = poem.text
            else:
                poem = None
            

            data.append({"title": title, "author": author, "summary": summary, "poem": poem, "link": link})

    df = pd.DataFrame(data)  # create a dataframe
    df.to_csv('poems.csv', mode='a', header=False, index=False)  # export to csv file
    return df 
               