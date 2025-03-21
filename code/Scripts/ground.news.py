import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

URL = "https://www.lbc.co.uk/crime/"
BASE_URL = "https://www.lbc.co.uk"


def fetch_lbc_news(url):
    news_list = []

    try:
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Extract news articles
        news = soup.find_all('div', class_='article editorial promo long-form')

        for new in news:
            headline = new.find('h3').text.strip() if new.find('h3') else "No headline"
            link = new.find('a')['href'] if new.find('a') else "#"
            link = link if link.startswith('http') else BASE_URL + link
            img_url = new.find('img')['src'] if new.find('img') else "No image"

            print(f"Fetching article: {headline}")

            # Navigate to article page
            driver.get(link)
            time.sleep(2)
            article_html = driver.page_source
            article_soup = BeautifulSoup(article_html, 'html.parser')

            standfirst = article_soup.find('p', class_="standfirst")
            standfirst = standfirst.text.strip() if standfirst else "No standfirst"

            content = article_soup.find_all('p', class_="paragraph-text")
            content = ' '.join(c.text.strip() for c in content) if content else "No content"

            author = article_soup.find('p', class_="author-details__author")
            author = author.text.strip() if author else "Unknown author"

            publish_date = article_soup.find('p', class_="publish_date")
            publish_date = publish_date.text.strip() if publish_date else "No publish date"

            # Append to list
            news_list.append({
                'headline': headline,
                'link': link,
                'img_url': img_url,
                'standfirst': standfirst,
                'content': content,
                'author': author,
                'publish_date': publish_date
            })

        # Save to CSV
        df = pd.DataFrame(news_list)
        df.to_csv('lbc_news.csv', index=False)
        print("News data saved successfully.")

        return df

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        driver.quit()

fetch_lbc_news(URL)



# url = "https://www.lbc.co.uk/crime/"
# BASE_URL = "https://www.lbc.co.uk"

# def fetch_ibc_news(url):
#     news_list = []
#     footer_lnks = []
#     driver.get(url)
#     time.sleep(2)
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'html.parser')
    

#     news = soup.find_all('div', class_='article editorial promo long-form')
#     # print(len(news))
#     for new in news:
#         headline = new.find('h3').text
#         link = new.find('a')['href']
#         if link == None:
#             link = 'No link'
#         else:

#             link = BASE_URL + link
#         img_url = new.find('img')['src']
#         if img_url == None:
#             img_url = 'No image'
#         else:
#             img_url = img_url

#         print(img_url)
#         print(headline)
#         print(link)
#         print('-------')

#         driver.get(link)
#         time.sleep(2)
#         html = driver.page_source
#         soup = BeautifulSoup(html, 'html.parser')
#         standfirst  = soup.find('p', class_ = "standfirst")
#         if standfirst == None:
#             standfirst = 'No standfirst'
#         else:
#             standfirst = standfirst.text

#         content = soup.find_all('p', class_ = "paragraph-text")
#         if content == None:
#             content = 'No content'
#         else:
                
#             content = [c.text for c in content]
#             content = ' '.join(content)
#         print(standfirst)
#         print(content)
#         print('+++++++++++++++++++++++++++++++++')



#         author = soup.find('p', class_ = "author-details__author")
#         if author == None:
#             author = 'No author'
#         else:
                
#             author = author.text if author else np.nan

#         publish_date = soup.find('p', class_ = "publish_date")
#         if publish_date == None:
#             publish_date = 'No publish_date'
#         else:
#             publish_date = publish_date.text
            
#         print(publish_date)
#         print(author)

#         news_list.append({
#             'headline': headline,
#             'link': link,
#             'img_url': img_url,
#             'standfirst': standfirst,
#             'content': content,
#             'author': author,
#             'publish_date': publish_date
#         })
        
#     # Save to CSV
#     df = pd.DataFrame(news_list)
#     df.to_csv('lbc_news_v2.csv', index=False)
#     print("News data saved successfully.")


#     return df


# news_list = []
# footer_lnks = []
# driver.get(url)
# time.sleep(2)
# html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')

# footer_links  = soup.find_all('li', class_="footer-hot-links__item")
# for link in footer_links:
#     link = link.find('a')['href']
#     if 'https' not in link:
#         link = BASE_URL + link
#     footer_lnks.append(link)
        
# print(footer_lnks)
# for link in footer_lnks:
#     fetch_ibc_news(link)
#     time.sleep(2)
#     print('++++++++++++++')