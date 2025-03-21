from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
from ydata_profiling import ProfileReport
import requests
import re
# Set up Selenium WebDriver with headless mode

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
options.add_argument("--window-size=1920x1080")  # Set a large window size to avoid hidden elements
driver = webdriver.Chrome(options=options)

url = 'https://www.afro.who.int/health-topics'
BASE_URL = 'https://www.afro.who.int'

data = []
def get_page(url):
    driver.get(url)
    time.sleep(2)
    #     return driver.page_source
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # get the links
    links = soup.find_all('span', class_= 'field-content')
    print(len(links))
    links = [link.find('a')['href'] for link in links] 
    links = [BASE_URL + link for link in links]

    title = soup.find_all('span', class_='field-content')
    title = [t.text for t in title]

    # print(links)
    # print(title)
    # print('----------------')

    # get the content
    for i, link in enumerate(links):
        driver.get(link)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find_all('div', class_='views-row')
        # <li class="active"><span>Overview</span></li>


        # barner_related_links = soup.find('div', class_='simple-tab-display')
        # barner_related_links = barner_related_links.find_all('a')
        # barner_related_links = [link['href'] for link in barner_related_links]
        # barner_related_links = [BASE_URL + link for link in barner_related_links]

        banner = soup.find_all('span')
        for b in banner:
                
            if b.text == 'Overview':
                overview = soup.find('div', class_='simple-tab-display').text
                
            else:
                overview = "NaN"
        # print(barner_related_links)
        # print(len(barner_related_links))

        fact_sheet = soup.find('div', class_= 'region region-content').text
        print('----------------')
        # paragraphs = soup.find_all('div', class_='paragraph paragraph--type--factsheet paragraph--view-mode--default')
        # for p in paragraphs:
        #     print(p.text)
        #     print('----------------')

        # print(overview)
        # print(len(overview))
        print("-----------------------------------")
        print(fact_sheet)

        data.append({'title': title[i], 'overview': overview, 'content': fact_sheet, 'link': link})
    df = pd.DataFrame(data)
    df.to_csv('who_africa.csv', index=False)
    print('Saved to csv')

    return df

if __name__ == '__main__':
    
    get_page(url)
    print(f"Total news releases scraped: {len(data)}")  
    print('Done')
    driver.quit()   
    
