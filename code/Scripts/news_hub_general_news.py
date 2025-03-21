from urllib.parse import urljoin  
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from bs4 import BeautifulSoup  
import pandas as pd  
import time  

topics = ['breaking-news', 'trending','business','entertainment','politics','health', 'celebrities', 'economy','sports']  

def setup_driver():  
    """Configure and return a headless Chrome driver"""  
    options = webdriver.ChromeOptions()  
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")  
    options.add_argument("--no-sandbox")  
    options.add_argument("--disable-dev-shm-usage")  
    options.add_argument("--window-size=1920x1080")  
    
    return webdriver.Chrome(options=options)  

def get_titles_links(driver, url):  
    """Return the page source of the given URL"""  
    try:  
        driver.get(url)  
        html = driver.page_source  
        soup = BeautifulSoup(html, "html.parser")  
        articles = soup.find_all("article", class_='l-post grid-post grid-base-post')  
        
        data = []  
        for post in articles:  
            title = post.find("h2", class_="is-title post-title").text  
            link = post.find("h2").find("a")["href"]  
            data.append({"title": title, "link": link})  
        
        # Check if there's a next page  
        next_page = soup.find("a", class_="next page-numbers")  
        return data, next_page is not None  
    
    except Exception as e:  
        print(f"Error fetching page: {e}")  
        return [], False  

def get_page(driver, url):  
    """Return the page source of the given URL"""  
    try:  
        driver.get(url)  
        html = driver.page_source  
        soup = BeautifulSoup(html, "html.parser")  
        content = soup.find('div', class_='post-content cf entry-content content-spacious')  
        if content:  
            paragraphs = content.find_all('p')  
            return ' '.join([p.text for p in paragraphs])  
        return ""  
    except Exception as e:  
        print(f"Error fetching content: {e}")  
        return ""  

def main():  
    driver = setup_driver()  
    all_data = []  
    
    for topic in topics:  
        page = 1  
        has_next_page = True  
        
        while has_next_page:  
            url = f'https://newshub.co.ke/category/{topic}/page/{page}/'  
            articles, has_next_page = get_titles_links(driver, url)  
            
            for article in articles:  
                content = get_page(driver, article['link'])  
                all_data.append({  
                    "title": article['title'],  
                    "link": article['link'],  
                    "content": content  
                })  
            
            page += 1  
            time.sleep(1)  
    
    driver.quit()  
    
    # Convert data to DataFrame and save to CSV  
    df = pd.DataFrame(all_data)  
    df.to_csv('news_articles_v2.csv', index=False)  
    print("Data has been saved to news_articles.csv")  

if __name__ == "__main__":  
    main()  