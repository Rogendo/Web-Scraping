import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from selenium.common.exceptions import TimeoutException

url = 'https://www.news-medical.net/medical-a-z.aspx'
BASE_URL = 'https://www.news-medical.net/'
PAGE_LOAD_TIMEOUT = 25 

def setup_driver():
    driver = Chrome()
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver

driver = setup_driver()

def is_404_page(soup):
    """Check if current page is a 404 error page"""
    error_div = soup.find('div', class_='error404')
    return error_div is not None

def get_links_title(url):
    driver.get(url)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'expand-item')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    data_entries = []
    for block in soup.find_all('div', class_='expand-item'):
        for item in block.find_all('a'):
            title = item.text.strip()
            link = urljoin(BASE_URL, item['href'])
            
            # Skip obviously invalid links
            if '/tag/' in link or '/author/' in link:
                continue
                
            content, author = get_content(link)
            if content and author:  # Only add valid entries
                data_entries.append((title, link, content, author))
            time.sleep(1.5)  # Reduced delay since we're skipping invalid pages
            
    return data_entries

def get_content(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'content')))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Check for 404 page first
        if is_404_page(soup):
            print(f"Skipping 404 page: {url}")
            return None, None
            
        # Extract content
        content_div = soup.find('div', class_='content')
        content = content_div.text.strip() if content_div else None
        
        # Extract author
        author_span = soup.find('span', class_='article-meta-author')
        author = author_span.text.strip() if author_span else None
        
        if not content or not author:
            print(f"Incomplete page: {url}")
            return None, None
            
        return content, author
        
    except TimeoutException:
        print(f"Timeout loading page: {url}")
        return None, None
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return None, None

def main():
    data = []
    try:
        entries = get_links_title(url)
        valid_entries = [entry for entry in entries if all(entry)]
        
        for title, link, content, author in valid_entries:
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
        df.to_csv('news_medical_valid.csv', index=False)
        print(f"Successfully saved {len(data)} valid articles")
    else:
        print("No valid articles found")

if __name__ == '__main__':
    main()