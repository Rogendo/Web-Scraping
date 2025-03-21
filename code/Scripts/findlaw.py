from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import requests


chrome_options = Options()

chrome_options.headless = True
driver = webdriver.Chrome(options=chrome_options)


def scrape_findlaw_blogs():
    """
    Get the blogs from findlaw.com
    """
    try:
        # links = df_3['link']
        # link = 'https://www.findlaw.com/legalblogs/legally-weird/'
        # driver.get(link)
        # soup = BeautifulSoup(driver.page_source, 'html.parser')
        # blogs = soup.find_all('div', class_='preview-column')
        for link in df_3:
            driver.get(link)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            blogs = soup.find_all('div', class_= 'preview-content')
                       
            
            blog_list = []

            for blog in blogs:
                title = blog.find('h2', class_='preview-title-blogs').text
                author = blog.find('div', class_='authorByline').text
                # date = blog.find('span', class_='date').text
                link = blog.find('a')['href']
                summary = blog.find('p', class_='preview-text').text
                readmore = blog.find('a', class_='preview-button fl-button fl-link-button secondary')
                readmore = readmore['href']
                # print(readmore)
                content = requests.get(readmore)
                content = BeautifulSoup(content.text, 'html.parser')
                content = content.find('div', class_='extra-row-spacing')
                content = get_content(link)

                
                blog_list.append({
                    'title': title,
                    'author': author,
                    # 'date': date,
                    'link': link,
                    'summary': summary,
                    'content': content
                })

            df = pd.DataFrame(blog_list)
            df.to_csv('findlaw_blogs.csv', index=False)

        return blog_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_more_articles():
    """
    Get more articles from findlaw.com and accumulate all pages' articles.
    """
    articles_list = []  # Initialize outside the loop to accumulate all articles
    try:
        url = "https://www.findlaw.com/legalblogs/law-and-life/"
        max_pages = 1680  # Adjust this value to scrape more pages
        
        for i in range(1, max_pages + 1):  # Include max_pages by adjusting the range
            page_url = f"{url}page/{i}/"
            driver.get(page_url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            articles_on_page = soup.find_all('div', class_='preview-content')
            
            for article in articles_on_page:
                title = article.find('h2').text.strip()
                link = article.find('a')['href']
                author_element = article.find('div', class_='authorByline')
                author = author_element.text.strip() if author_element else "Unknown"
                summary_element = article.find('p', class_='preview-text')
                summary = summary_element.text.strip() if summary_element else ""
                content = get_content(link)
                
                articles_list.append({
                    'title': title,
                    'author': author,
                    'link': link,
                    'summary': summary,
                    'content': content
                })

        # Save all articles to CSV after processing all pages
        df = pd.DataFrame(articles_list)
        df.to_csv('findlaw_more_articles.csv', index=False)
        return articles_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_content(url):
    """
    Get the content of the articles
    """
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.find('div', class_='g-col-12 g-col-md-10 g-start-md-2 g-col-xxl-9 g-start-xxl-1')
        content = content.text
        # print(content)
        return content
        


    except Exception as e:
        print(f"An error occurred: {e}")
        return None


url = "https://www.findlaw.com/legalblogs/"
# get_content()
# scrape_findlaw_blogs()

if __name__ == "__main__":
    get_more_articles()
    driver.quit()