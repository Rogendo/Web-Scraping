import time
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

# Initialize base URL for joining relative links
base_url = "https://www.news-medical.net"

def setup_driver():
    
    from selenium import webdriver
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(options=options)
    return driver

def get_article_info(url, driver):
    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find article content
        content = soup.find('div', class_='content') or soup.find('div', class_='item-body newsguard-body')
        return content.text if content else "NaN"
    except Exception as e:
        print(f"Error retrieving article content: {e}")
        return "NaN"

def get_articles(url, driver):
    data = []
    try:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('div', class_='row')

        for article in articles:
            title = article.find('h3')
            title = title.text.strip() if title else "NaN"

            link = article.find('a', href=True)
            article_url = urljoin(base_url, link['href']) if link else None

            content = get_article_info(article_url, driver) if article_url else "NaN"

            print(f"Title: {title}")
            print(f"Link: {article_url}")
            print(f"Content length: {len(content)} characters")
            print('-----------------')

            data.append({
                'title': title,
                'link': article_url,
                'content': content
            })
    except Exception as e:
        print(f"Error processing page {url}: {e}")
    
    return data

def main():
    driver = setup_driver()
    all_data = []
    
    links = [
        'https://www.news-medical.net/medical/interviews',
        'https://www.news-medical.net/medical/thought-leaders?page=49',
        'https://www.news-medical.net/medical/insights-from-industry?page=29',
        'https://www.news-medical.net/medical/news?page=3',
        'https://www.news-medical.net/medical/whitepapers?page=49',
        'https://www.news-medical.net/mediknowledge?page=4',
        'https://www.news-medical.net/mediknowledge',
        # "https://www.news-medical.net/medical/articles",
    ]

    # Process unique base URLs
    unique_base_urls = {url.split('?')[0] for url in links}
    
    for base_url in unique_base_urls:
        page_num = 1
        while True:
            page_url = f"{base_url}?page={page_num}"
            print(f"\nProcessing: {page_url}")
            
            page_data = get_articles(page_url, driver)
            
            if not page_data:
                print(f"No articles found on page {page_num}. Ending pagination.")
                break
            
            all_data.extend(page_data)
            page_num += 1

    # Save all collected data to CSV
    df = pd.DataFrame(all_data)
    df.to_csv('med_news_v6.csv', index=False)
    print("Data saved successfully.")
    
    driver.quit()

if __name__ == '__main__':
    main()