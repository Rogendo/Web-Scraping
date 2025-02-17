from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd

BASE_URL = "https://dev.to/"

def get_article_content(article_url):
    """Fetch the full article content from the article page using requests."""
    try:
        response = requests.get(article_url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the main content from the article page
        content_div = soup.find("div", class_="crayons-article__main")
        if content_div:
            content = " ".join([p.text.strip() for p in content_div.find_all("p")])
        else:
            content = "Content not found"
    except Exception as e:
        content = f"Error fetching content: {e}"
    return content

def scroll_page(driver, pause_time=2, max_scrolls=10):
    """Scrolls through the page to load dynamic content."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_scrolls):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the new content
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_articles(url):
    """Scrape the homepage for article links and details after simulating scrolling."""

    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url)
    time.sleep(2)  
    # Scroll to load dynamic content
    scroll_page(driver, pause_time=2, max_scrolls=10)

    # Get the page source after scrolling
    html = driver.page_source
    driver.quit()

    # Parse the loaded page with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("div", class_="crayons-story")

    data = []
    for article in articles:
        # Extract title
        title_tag = article.find("h2", class_="crayons-story__title")
        title = title_tag.text.strip() if title_tag else "No title"

        # Extract article link; note that links on dev.to may be relative.
        link_tag = title_tag.find("a") if title_tag else None
        if link_tag and link_tag.has_attr("href"):
            # If the link is relative, prepend BASE_URL if needed.
            href = link_tag['href']
            if not href.startswith("http"):
                link = f"https://dev.to{href}"
            else:
                link = href
        else:
            link = "No link"

        # Extract author
        author_tag = article.find("a", class_="crayons-story__secondary")
        author = author_tag.text.strip() if author_tag else "Unknown"

        # Extract date
        date_tag = article.find("a", class_="crayons-story__tertiary")
        date = date_tag.text.strip() if date_tag else "No date"

        # Extract hashtags
        hashtag_tags = article.find_all("a", class_="crayons-tag")
        hashtags = ", ".join([tag.text.strip() for tag in hashtag_tags]) if hashtag_tags else "No hashtags"

        # Fetch full article content by visiting the article page if we have a valid link.
        if link.startswith("http"):
            content = get_article_content(link)
        else:
            content = "No content (Invalid link)"

        data.append([title, link, author, date, content, hashtags])

    # Convert list of data to a pandas DataFrame
    df = pd.DataFrame(data, columns=["Article Title", "Article Link", "Author", "Date", "Content", "Hashtags"])
    return df
def get_articles_from_page(url):
    """Scrape a single page given by the URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("div", class_="crayons-story")
    
    data = []
    for article in articles:
        title_tag = article.find("h2", class_="crayons-story__title")
        title = title_tag.text.strip() if title_tag else "No title"

        link_tag = title_tag.find("a") if title_tag else None
        if link_tag and link_tag.has_attr("href"):
            href = link_tag['href']
            link = f"https://dev.to{href}" if not href.startswith("http") else href
        else:
            link = "No link"

        author_tag = article.find("a", class_="crayons-story__secondary")
        author = author_tag.text.strip() if author_tag else "Unknown"

        date_tag = article.find("a", class_="crayons-story__tertiary")
        date = date_tag.text.strip() if date_tag else "No date"

        hashtag_tags = article.find_all("a", class_="crayons-tag")
        hashtags = ", ".join([tag.text.strip() for tag in hashtag_tags]) if hashtag_tags else "No hashtags"

        # For each article, get the content from its individual page.
        if link.startswith("http"):
            content = get_article_content(link)
        else:
            content = "No content (Invalid link)"
        
        data.append([title, link, author, date, content, hashtags])
    
    return data

def get_all_articles(max_pages=10000):
    """Iterate over several pages and return a DataFrame of all articles."""
    all_data = []
    for page in range(1, max_pages+1):
        print(f"Processing page {page}...")
        page_url = f"https://dev.to/?page={page}"
        page_data = get_articles_from_page(page_url)
        all_data.extend(page_data)
        time.sleep(2)  # be kind to the server :)
    
    df = pd.DataFrame(all_data, columns=["Article Title", "Article Link", "Author", "Date", "Content", "Hashtags"])
    return df

df_articles = get_all_articles(max_pages=3650)  
print(df_articles)


df_articles.to_csv('dev.to_blog.csv', index=False)

