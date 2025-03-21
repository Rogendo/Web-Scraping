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

url = 'https://www.emro.who.int/health-topics.html'  
BASE_URL = 'https://www.emro.who.int'  


def convert_http_to_https(links):  
    """Convert HTTP links to HTTPS."""  
    return [link.replace('http://', 'https://') if link.startswith('http://') else link for link in links]  

def get_emro_health_topics(url):  
    driver = setup_driver()  
    driver.get(url)  
    time.sleep(2)  
    html = driver.page_source  
    soup = BeautifulSoup(html, 'html.parser')  

    letters_div = soup.find('div', class_='col span_6_of_12')  
    links = [urljoin(BASE_URL, a['href']) for a in letters_div.find_all('a', href=True)]  
    links = convert_http_to_https(links)  

    titles = [t.text.strip() for t in letters_div.find_all('a') if t.text.strip() != '']  
    
    print(len(links))  
    print(len(titles))  
    print(links)  
    print(titles)  
    print('----------------')  
    
    driver.quit()  
    return links, titles  

def get_content(url, driver):  
    try:  
        driver.get(url)  
        # Wait up  for the content to load  
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'div.article-content'))  
        WebDriverWait(driver, 10).until(element_present)  
        html = driver.page_source  
        soup = BeautifulSoup(html, 'html.parser')  
        content_div = soup.find('div', class_='article-content')  
        if content_div is None:  
            return 'Content not available'  
        return content_div.text  
    except Exception as e:  
        print(f"An error occurred: {e}")  
        return 'Content not available'  

def main():  
    links, titles = get_emro_health_topics(url)  
    data = []  
    driver = setup_driver()  
    for i, link in enumerate(links):  
        content = get_content(link, driver)  
        data.append({'title': titles[i], 'content': content, 'link': link})  
    driver.quit()  
    return data  

if __name__ == '__main__':  
    data = main()  
    print('Done')  
    df = pd.DataFrame(data)  
    df.to_csv('who_emro_health_topics_V2.csv', index=False)  
    print('Saved to csv')  