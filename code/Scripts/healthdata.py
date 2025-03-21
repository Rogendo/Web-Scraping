from urllib.parse import urljoin  
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from bs4 import BeautifulSoup  
import pandas as pd  
import time  

def setup_driver():  
    """Configure and return a headless Chrome driver"""  
    options = webdriver.ChromeOptions()  
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")  
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage")  
    options.add_argument("--window-size=1920x1080")  
    
    return webdriver.Chrome(options=options)  

driver = setup_driver()


base_urls = [
    'https://healthdata.gov/browse?category=Health&sortBy=last_modified&utf8=%E2%9C%93&pageSize=20&page=1',
    'https://healthdata.gov/browse?category=Blog&sortBy=last_modified&utf8=%E2%9C%93&page={page}&pageSize=20',
    'https://healthdata.gov/browse?category=Community&sortBy=last_modified&utf8=%E2%9C%93&pageSize=20',
    'https://healthdata.gov/browse?category=Hospital&sortBy=last_modified&utf8=%E2%9C%93&pageSize=20',
    'https://healthdata.gov/browse?category=National&sortBy=last_modified&utf8=%E2%9C%93&pageSize=20',

    ]
    
# base_url = "https://healthdata.gov/browse?category=Blog&sortBy=last_modified&utf8=%E2%9C%93&page={page}&pageSize=20"

# List to hold all extracted data
blog_data = []

total_pages = 70  # Adjust to scrape more pages if needed

def get_content(url):
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    content = soup.find('div', class_='react-grid-layout grid-layout')
    if content is not None:
        content = content.text
        # print(content)
    else:
        content = soup.find('div', class_='description-section')
        if content is not None:
            content = content.text
            # print(content)
        else:
            content = soup.find('div', class_='block')
            if content is not None:
                content = content.text
                # print(content)
            else:
                content = 'NaN'
                # print(content)

    return content

def get_data(base_url):
    for page_num in range(1, total_pages + 1):
        driver.get(base_url.format(page=page_num))
        
        # Wait for the page to load 
        time.sleep(2)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        blog_posts = soup.find_all('div', class_='asset-card')  
        
        # Loop through each blog post and extract data
        for post in blog_posts:
            title = post.find('h3', class_='entry-name forge-typography--headline5') 
            description = post.find('div', class_='collapsed-text-section')
            url = post.find('a', href=True, class_='entry-name-link')
            url = url['href'] if url else ''
            # print(url)
            content = get_content(url)
            print(content)
            
            blog_data.append({
                'title': title.get_text(strip=True) if title else '',
                'description': description.get_text(strip=True) if description else '',
                'url': url,
                'content': content
            })
        
        print(f"Page {page_num} scraped.")

    driver.quit()

    # Save the data to a CSV file
    df = pd.DataFrame(blog_data)
    df.to_csv('scraped_health_blogs_v8.csv', index=False)

    print("Scraping complete! Data has been saved to 'scraped_health_blogs_v4.csv'.")

def main():
    for base_url in base_urls:
        get_data(base_url)

if __name__ == '__main__':
    main()
    