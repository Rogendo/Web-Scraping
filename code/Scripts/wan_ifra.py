import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from selenium.common.exceptions import TimeoutException

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

def scrape_all_news_pages():
    page_num = 1
    extracted_data = []  # List to store extracted data
    
    while True:
        if page_num == 1:
            url = 'https://wan-ifra.org/insights'
        else:
            url = f'https://wan-ifra.org/insights/page/{page_num}/'
        
        driver.get(url)
        time.sleep(2)  
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        posts = soup.find_all('div', class_='post')
        
        # Stop if no posts found
        if not posts:
            print(f"No more posts on page {page_num}. Exiting.")
            break
        
        print(f"Scraping page {page_num}...")
        for post in posts:
            # Extract title and link with error handling
            title_element = post.find('h1')
            link_element = post.find('a')
            
            if title_element and link_element:
                title = title_element.get_text(strip=True)
                link = link_element.get('href')
                article_info, content = get_article_content(link)

                
                # Add the extracted data to the list
                extracted_data.append([title, link, article_info, content])
                print(f"Title: {title}\nLink: {link}\nArticleInfo {article_info}\n")
                
        
        page_num += 1
    
    # Save the extracted data to CSV
    save_to_csv(extracted_data)

def get_article_content(url):
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    article_info = soup.find('p', class_='info').text

    content = soup.find('div', class_='content-area')
    content = content.text
    content = content.replace(article_info, ' ')
    return article_info, content

def save_to_csv(data):
    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=['Title', 'Link', 'article_info', 'content'])
    
    # export DataFrame to a CSV file
    df.to_csv('wan_ifra_insights.csv', index=False)
    print("Data has been saved to 'scraped_data.csv'.")

# Start scraping
scrape_all_news_pages()

driver.quit()
