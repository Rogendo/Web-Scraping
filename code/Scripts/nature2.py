from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup

# Set up Selenium with headless Chrome
chrome_options = Options()

chrome_options.headless = True
driver = webdriver.Chrome(options=chrome_options)

def get_journal_index():
    """
    This function scrapes the Nature Climate Change website for journals on a given page."""
    url = "https://www.nature.com/siteindex"

    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    journals = soup.find_all("li", class_="grid mq640-grid-12 text13 pa0 grid-6")
    journal_last = soup.find_all("li", class_="grid mq640-grid-12 text13 pa0 grid-6 last")
    journals.extend(journal_last)
    
    journal_list = []
    for journal in journals:
        
        title = journal.find("a").text
        link = journal.find("a")["href"]
        link = f"https://www.nature.com{link}"
        journal_list.append({"title": title, "link": link})

    return pd.DataFrame(journal_list)

def get_journal_articles(url):
    """
    This function scrapes the Nature Climate Change website for articles published in a given journal.
    
    Parameters:
    link: str, the URL of the journal
    
    return: DataFrame, a DataFrame containing the title, authors, and summary of the articles in the journal

    """
    driver.get(url)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all("div", class_="u-full-height")
    article_list = []
    for article in articles:
        title = article.find("h3", class_="c-card__title").text
        link = article.find("a", class_="c-card__link u-link-inherit")["href"]
        link = f"https://www.nature.com{link}"
        print(link)

        authors = article.find_all("ul", class_="c-author-list c-author-list--compact c-author-list--truncated")
        authors = [author.text for author in authors]
        authors_tags = article.find_all("ul", class_="c-author-list c-author-list--compact c-author-list--truncated")
        authors = []
        for author_tag in authors_tags:
            author_names = author_tag.find_all("li")
            authors.extend([author_name.text.strip() for author_name in author_names])
        if not authors:
            authors = ["No authors"]
        # summary = article.find("div", class_="c-card__summary").text
        # summary = article.find("div", class_="c-card__summary").text
        # abstract  
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        abstract = soup.find("div", class_="c-article-section__content")
        if abstract:
            abstract = abstract.text
        else:
            abstract = "No content"
        reference = soup.find("p", class_="c-article-references__text")
        if reference:
            reference = reference.text
        else:
            reference = "No content"
        
        content = soup.find("div", class_="main-content")
        if content:
            content = content.text
        else:
            content = "No content"

        article_list.append({"title": title, "authors": authors, "link": link,"abstract":abstract, "content":content, "reference": reference})
    return pd.DataFrame(article_list)

# Loop through the links extracted from the df_index DataFrame

all_journal_data = []
for link in df_index['link']:
    try:
        df = get_journal_articles(link)
        all_journal_data.append(df)
        print(f"Extracted data for journal: {link}")
    except requests.exceptions.ReadTimeout:
        print(f"Read timeout occurred for journal: {link}")
    except Exception as e:
        print(f"An error occurred for journal: {link} - {e}")

# Concatenate all data into a single DataFrame
all_journal_data = pd.concat(all_journal_data, ignore_index=True)

'''
extracts the regional Nature websites from the Nature Climate Change website.
    These regions include:

    Nature Africa
    Nature China
    Nature India
    Nature Italy
    Nature Japan
    Nature Middle East
'''
urls = ["https://www.nature.com/natafrica","https://www.nature.com/nindia","https://www.nature.com/natitaly","https://www.natureasia.com/ja-jp","https://www.nature.com/nmiddleeast"]
for url in urls:
    df = get_journal_articles(url)
    all_journal_data.append(df)
    

# Save the concatenated DataFrame to a single CSV file
all_journal_data.to_csv("all_journal_articles.csv", index=False)
print("Saved all_journal_articles.csv")
# Close the Selenium driver
driver.quit()