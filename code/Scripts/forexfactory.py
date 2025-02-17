from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

url = "https://www.forexfactory.com/news/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def extract_fx_brokers(url):
    pass

def extract_fx_news(url):
    pass

def extract_fx_calendar(url):
    pass


class FX_Pairs:
        
    def extract_fx_prices():
        '''
        Extracts forex prices from the Forex Factory API
        '''
        url = "https://mds-api.forexfactory.com/bars?to=0&interval=M5&instrument=EUR%2FUSD&per_page=200&extra_fields="

        try:
            response = requests.get(url, timeout=10, headers=headers)
            response.raise_for_status()
            data = response.json()
            print("Response JSON:", data)  # Debug print statement
            df = pd.DataFrame(data['data'])
            df.to_csv("forexfactory_forex_prices.csv", index=False)
            return df
        
        except Exception as e:
            print(f"Error processing {url}: {e}")
            return pd.DataFrame()
    
    # def 

df=FX_Pairs.extract_fx_prices()
print(df.head())
print(df.shape)

def extract_fx_analysis(url):
    pass


def extract_fx_trades(url):
    pass

def extract_fx_forum(url):
    pass

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

