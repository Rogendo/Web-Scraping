from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import requests
from ydata_profiling import ProfileReport
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException


# Set up Selenium WebDriver with headless mode

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
options.add_argument("--window-size=1920x1080")  # Set a large window size to avoid hidden elements
driver = webdriver.Chrome(options=options)



def scrape_nairobilawmonthly_data():
    urls = [
        "https://nairobilawmonthly.com/category/briefing/",
        "https://nairobilawmonthly.com/category/business/",
        "https://nairobilawmonthly.com/category/essayseditorial/",
        "https://nairobilawmonthly.com/category/special-reports/",
        "https://nairobilawmonthly.com/category/life/"
    ]
    data = []

    for url in urls:
        driver.get(url)
        time.sleep(3)  # Initial wait to let the page load

        # Click all "LOAD MORE" buttons until none remain
        while True:
            try:
                more_btn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, "LOAD MORE"))
                )
                driver.execute_script("arguments[0].scrollIntoView();", more_btn)
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, "LOAD MORE")))
                more_btn.click()
                time.sleep(3)  # Wait for new content to load
            except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
                print("No more 'LOAD MORE' buttons or element refreshed.")
                break  # Exit the loop when no more button is found

        # Parse articles after all content is loaded
        soup = BeautifulSoup(driver.page_source, "html.parser")
        articles = soup.find_all("article", class_="l-post list-post list-post-on-sm m-pos-left")

        for article in articles:
            try:
                title = article.find("h2", class_="is-title post-title").get_text(strip=True)
                link = article.find("a")["href"]
                # content = get_nairobilawmonthly_content(link)

                data.append({"title": title, "link": link})
            except AttributeError:
                print("Skipping an article due to missing elements.")

    # Convert data to a DataFrame
    df = pd.DataFrame(data)
    return df

def get_nairobilawmonthly_content(url):
    driver.get(url)
    time.sleep(3) 

    # Parse the article content
    soup = BeautifulSoup(driver.page_source, "html.parser")
    content = soup.find("div", class_="post-content-wrap has-share-float has-share-float-in").text

    return content
# Run the scraper
# df = scrape_nairobilawmonthly_data()
# print(df)

driver.quit()

df = scrape_nairobilawmonthly_data()
df.to_csv('nairobilawmonthly.csv',index=False)

