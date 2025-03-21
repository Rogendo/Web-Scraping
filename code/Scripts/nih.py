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

url = "https://www.nih.gov/news-events/news-releases"  
BASE_URL = 'https://www.nih.gov'

def scrape_nih():  
    """Scrapes detailed news articles from the NIH news page."""  
    driver.get(url)  
    time.sleep(2)  
    html = driver.page_source  
    soup = BeautifulSoup(html, 'html.parser')  
    titles = soup.find_all('li', class_="views-row")  

    # Get titles from pagination
    titles.extend(nih_next_page())

    data = []  
    article_titles = []

    for title in titles:  
        try:
            article_link = title.find('h4', class_="teaser-title").find('a')['href']  
            article_link = BASE_URL + article_link  
            pub_date = title.find('span', class_='date-display-single').text  
            article_summary = title.find('p', class_='teaser-description').text.replace(pub_date, '')  
            
            # Navigate to article page  
            driver.get(article_link)  
            time.sleep(2)  
            html = driver.page_source  
            soup = BeautifulSoup(html, 'html.parser')  
            article_title = soup.find('h1').text  
            article_titles.append(article_title)

            featured_media = soup.find_all('picture')  
            featured_media = featured_media[0].find('img')['src'] if featured_media else 'Nan'  

            article_content = ' '.join([p.text for p in soup.find_all('p')])  
            article_content = article_content.replace(pub_date, '')  
            article_content = article_content.replace(featured_media, '')  
            
            data.append({  
                'title': article_title,  
                'article_link': article_link,  
                'pub_date': pub_date,  
                'article_summary': article_summary,  
                'featured_media': featured_media,  
                'article_content': article_content  
            })  
        except Exception as e:
            print(f"Error scraping article: {e}")

    df = pd.DataFrame(data)  
    df.to_csv('nih_articles.csv', index=False)  
    print(f"Total articles scraped: {len(article_titles)}")
    return article_titles  

def nih_next_page():  
    """Scrapes news articles from all available pages."""  
    all_titles = []  
    prev_length = 0

    while True:  
        html = driver.page_source  
        soup = BeautifulSoup(html, 'html.parser')  
        new_titles = soup.find_all('li', class_="views-row")
        
        all_titles.extend(new_titles)  

        print(f"Scraped {len(new_titles)} titles from {driver.current_url}")  

        try:  
            next_button = WebDriverWait(driver, 10).until(  
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.pager__item--next a'))  
            )  

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)  
            time.sleep(1)  

            driver.execute_script("arguments[0].click();", next_button)  

            WebDriverWait(driver, 10).until(  
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h4.teaser-title'))  
            )  
            print("New page content loaded.")  
            time.sleep(2)  

            if len(all_titles) == prev_length:  # Break if no new articles are found
                break
            prev_length = len(all_titles)

        except Exception as e:  
            print(f"No more 'next' button found or error: {e}")  
            break  

    print(f"Total titles scraped from all pages: {len(all_titles)}")  
    return all_titles  

if __name__ == '__main__':  
    all_news = scrape_nih()  
    print(f"Total news releases scraped: {len(all_news)}")  
    driver.quit()
