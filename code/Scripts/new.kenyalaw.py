import pandas as pd
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from docx import Document
import uuid
import re
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

# Configuration
years = ['2025', '2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '1992', '1991', '1990', '1989', '1988', '1987', '1986', '1985', '1984', '1983', '1982', '1981', '1980', '1979', '1978', '1977', '1976', '1975', '1974', '1972', '1971', '1970', '1969', '1967', '1966', '1964', '1961', '1954', '1944', '1938', '1930']
BASE_URL = "https://new.kenyalaw.org/judgments/all/{year}/?page={page}"
DOWNLOAD_DIR = 'valid_docs'
CSV_FILE = 'judgements_v2.csv'
MAX_RETRIES = 3

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def sanitize_filename(title):
    clean_title = re.sub(r'[^a-zA-Z0-9 \-\_\(\)]', '', title)
    clean_title = re.sub(r'\s+', '_', clean_title)[:50]
    return f"{clean_title}_{uuid.uuid4().hex[:6]}.docx"

def requests_session():
    session = requests.Session()
    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def process_judgment(session, link, title, driver):
    original_url = driver.current_url
    try:
        for attempt in range(MAX_RETRIES):
            try:
                driver.get(link)
                WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Download DOCX")]'))
                )
                docx_element = driver.find_element(By.XPATH, '//a[contains(text(), "Download DOCX")]')
                docx_url = docx_element.get_attribute('href')
                
                if not docx_url or not docx_url.endswith('.docx'):
                    print(f"No valid DOCX link for {title}")
                    return None

                filename = sanitize_filename(title)
                filepath = os.path.join(DOWNLOAD_DIR, filename)
                
                response = session.get(docx_url, stream=True, timeout=30)
                print(f"Downloading {docx_url} (Status: {response.status_code})")
                response.raise_for_status()

                if 'vnd.openxmlformats-officedocument.wordprocessingml.document' not in response.headers.get('Content-Type', ''):
                    print(f"Invalid content type for {title}")
                    return None

                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(8192):
                        f.write(chunk)

                try:
                    doc = Document(filepath)
                    content = '\n'.join(para.text for para in doc.paragraphs if para.text.strip())
                    return content
                except Exception as e:
                    print(f"Failed to read DOCX for {title}: {e}")
                    os.remove(filepath)
                    return None
                break
            except (TimeoutException, WebDriverException) as e:
                if attempt < MAX_RETRIES - 1:
                    print(f"Retrying {title} (Attempt {attempt + 1})")
                    time.sleep(2)
                    continue
                else:
                    raise
    except Exception as e:
        print(f"Error processing {title}: {str(e)} [URL: {link}]")
        return None
    finally:
        driver.get(original_url)
        time.sleep(1)

def scrape_judgments():
    driver = setup_driver()
    session = requests_session()
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    data = []

    try:
        for year in years:
            page = 1
            while True:
                current_url = BASE_URL.format(year=year, page=page)
                print(f"Processing: {current_url}")
                
                try:
                    driver.get(current_url)
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="doc-table"]/table'))
                    )
                except TimeoutException:
                    print(f"No data found for {year} page {page}")
                    break

                judgments = driver.find_elements(By.XPATH, '//*[@id="doc-table"]/table/tbody/tr')
                if not judgments:
                    break

                for judgment in judgments:
                    try:
                        title = judgment.find_element(By.XPATH, './/td').text.strip()
                        link = judgment.find_element(By.XPATH, './/td/a').get_attribute('href')
                    except NoSuchElementException:
                        continue

                    content = process_judgment(session, link, title, driver)
                    if content:
                        data.append({'title': title, 'link': link, 'content': content})
                        pd.DataFrame(data).to_csv(CSV_FILE, index=False)
                    time.sleep(1)

                try:
                    next_button = driver.find_element(By.XPATH, '//a[contains(text(), "Next")]')
                    if 'disabled' in next_button.get_attribute('class'):
                        break
                    page += 1
                except NoSuchElementException:
                    break
    finally:
        driver.quit()
        print("Scraping completed. Driver closed.")

if __name__ == "__main__":
    scrape_judgments()