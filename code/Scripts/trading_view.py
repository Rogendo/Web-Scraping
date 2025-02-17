from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

url = "https://www.tradingview.com/news/"

# function to extract news headlines and content from TradingView
def extract_trading_view(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all article containers
        articles = soup.find_all("div", class_="content-JhZ1X2FK")

        data = []
        for article in articles:
            headline_tag = article.find('a')  # Assuming headlines are in <a> tags
            if headline_tag:
                headline = headline_tag.get_text(strip=True)
                link = requests.compat.urljoin(url, headline_tag['href'])  # Convert relative link to absolute
                content = extract_page_content(link)
                data.append({"headline": headline, "link": link, "content": content})

        return pd.DataFrame(data)  # Return as a DataFrame 

    except Exception as e:
        print(f"Error processing {url}: {e}")
        return pd.DataFrame()

def extract_page_content(link):
    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all 'article' elements with class 'wrapper-pIO_GYwT'
        content_divs = soup.find_all("article", class_="wrapper-pIO_GYwT")
        
        content_list = []
        for div in content_divs:
            # Find all <p> tags inside the article, excluding ones with unwanted attributes if needed
            paragraphs = div.find_all(lambda tag: tag.name == "p")
            
            # Extract text from paragraphs and append to content list
            for p in paragraphs:
                content_list.append(p.get_text(strip=True))
        
        # Join all paragraph texts into a single string
        content = " ".join(content_list)
        
        return content if content else "No content found"

    except Exception as e:
        print(f"Error processing {link}: {e}")
        return "Error fetching content"


df = extract_trading_view(url)
print(df.head())

df.to_csv("tradingview_news.csv", index=False)
