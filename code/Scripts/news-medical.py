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


links = [
    'https://www.news-medical.net/medical/interviews',
    'https://www.news-medical.net/medical/thought-leaders?page=49',
    'https://www.news-medical.net/medical/insights-from-industry?page=29',
    'https://www.news-medical.net/medical/news?page=3',
    'https://www.news-medical.net/medical/whitepapers?page=49',
    'https://www.news-medical.net/mediknowledge?page=4',
    'https://www.news-medical.net/mediknowledge',
]

# url = 'https://www.news-medical.net/medical/news'

# def get_articles(url):
#     data = []
#     driver.get(url)
#     time.sleep(2)
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     articles = soup.find_all('div', class_='row')
#     for article in articles:
#         title = article.find('h3')
#         if title is None:
#             title = 'NaN'
#         else:
#             title = title.text.strip()

#         link = article.find('a')
#         if link is None:
#             link = 'NaN'
#         else:
#             link = link['href']
#             link = urljoin(base_url, link)

#         content = get_article_info(link)

#         print(title)
#         print(link)
#         print(content)
#         print('-----------------')

#         data.append({
#             'title': title,
#             'link': link,
#             'content': content
#         })
#     df = pd.DataFrame(data)
#     df.to_csv('med_news_v2.csv', index=False)

#     return data

driver = setup_driver()


def get_article_info(url):
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    content = soup.find('div', class_='content')
    if content == None:
        content = soup.find('div', class_='item-body newsguard-body')
        # content = content.text

        if content == None:
            content = "NaN"

    else:
        content = content.text
        
    return content
    
from urllib.parse import urljoin

base_url = "https://www.news-medical.net"

def get_articles(url):
    data = []
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all('div', class_='row')

    for article in articles:
        title = article.find('h3')
        title = title.text.strip() if title else "NaN"

        link = article.find('a')
        if link and 'href' in link.attrs:
            link = urljoin(base_url, link['href'])
        else:
            link = None  # Prevent invalid URLs

        content = get_article_info(link) if link else "NaN"

        print(title)
        print(link)
        print(content)
        print('-----------------')

        data.append({
            'title': title,
            'link': link,
            'content': content
        })

    df = pd.DataFrame(data)
    df.to_csv('med_news_v4.csv', index=False)
    return data



def main():
    links = ['https://www.news-medical.net/medical/interviews','https://www.news-medical.net/medical/thought-leaders', 'https://www.news-medical.net/medical/whitepapers', 'https://www.news-medical.net/mediknowledge']
    for url in links:
        get_articles(url)
        
    driver.quit()

if __name__ == '__main__':
    main()

    