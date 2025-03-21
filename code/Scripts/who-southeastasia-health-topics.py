# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


BASE_URL = 'https://www.who.int/southeastasia'
MAIN_URL = 'https://www.who.int/southeastasia/health-topics'

def setup_driver():
    """Configure and return a headless Chrome driver"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")
    
    return webdriver.Chrome( options=options)

data = []

def get_health_topics(driver):
    """Get all health topics from the main page"""
    driver.get(MAIN_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sf-content-block')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find('ul', class_='alphabetical-nav alphabetical-nav--list')
    link_tags = articles.find_all('a')
    links = [link['href'] for link in link_tags]
    topics = [link.text for link in link_tags]
    return topics, links

def extract_page_content(driver, url):
    """Extract content from a health topic page"""
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'sf-content-block')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.find('div', class_='sf-description large-body-font-size')
        # content = content.find_all('p')
        content = content.text
        # for p in content:
        #     p = p.text
            # if p.find('a'):
            #     p.a.decompose()

        # content = [p.text for p in content]
        return content
    except Exception as e:
        print(f'Error: {e}')
        
        content = 'Error'
        return content

def main():
    """ Main function to scrape the WHO - SouthEast Asia Health Topics page """
    data = []  # to hold the data we scrape
    driver = setup_driver()
    topics, links = get_health_topics(driver)
    for topic, link in zip(topics, links):
        content = extract_page_content(driver, link)
        data.append({
            'Topic': topic,
            'Link': link,
            'Content': content
        })
    driver.quit()
    return data

if __name__ == '__main__':
    data = main()
    print(data)
    df = pd.DataFrame(data)
    df.to_csv('southeast_asia_who_health_topics.csv', index=False)
    print('Data saved to southeast_asia_who_health_topics.csv')

