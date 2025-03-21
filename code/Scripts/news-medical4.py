import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from requests.exceptions import ReadTimeout

url = 'https://www.news-medical.net/medical-a-z.aspx'
BASE_URL = 'https://www.news-medical.net/'
MAX_RETRIES = 3  # Number of retry attempts for failed requests

def setup_driver():
    driver = Chrome()
    driver.implicitly_wait(10)  # Set default wait time for elements
    return driver

driver = setup_driver()

def get_links_title(url):
    driver.get(url)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'expand-item')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    question_blocks = soup.find_all('div', class_='expand-item')
    
    data_entries = []
    for block in question_blocks:
        for item in block.find_all('a'):
            title = item.text.strip()
            link = urljoin(BASE_URL, item['href'])
            content, author = get_content_with_retry(link)
            data_entries.append((title, link, content, author))
            time.sleep(2)  # Increased delay between requests
    return data_entries

def get_content_with_retry(url):
    for attempt in range(MAX_RETRIES):
        try:
            return get_content(url)
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {url}: {str(e)}")
            time.sleep(5 * (attempt + 1))  # Exponential backoff
    return "Content unavailable due to timeout", "Unknown author"

def get_content(url):
    try:
        driver.set_page_load_timeout(30)  # Set page load timeout to 30 seconds
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'content')))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content_div = soup.find('div', class_='content')
        content = content_div.text.strip() if content_div else 'Content not available'
        
        author_span = soup.find('span', class_='article-meta-author')
        author = author_span.text.strip() if author_span else 'Unknown author'
        
        return content, author
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        raise  # Re-raise exception for retry mechanism

def main():
    data = []
    try:
        entries = get_links_title(url)
        for title, link, content, author in entries:
            data.append({
                'title': title,
                'link': link,
                'content': content,
                'author': author
            })
    finally:
        driver.quit()
    
    if data:
        df = pd.DataFrame(data)
        df.to_csv('news_medical.csv', index=False)
        print(f"Saved {len(data)} articles to CSV.")
    else:
        print("No data was collected")

if __name__ == '__main__':
    main()