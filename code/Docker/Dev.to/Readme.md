# Dev.to Blog Scraper

This project contains a Python script to scrape articles from the Dev.to website. The script uses Selenium and BeautifulSoup to extract article details and content, and saves the data into a CSV file.

## Requirements

- Python 3.12
- Selenium
- BeautifulSoup4
- Requests
- Pandas
- Chrome WebDriver

## Installation and Usage


1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/devto-blog-scraper.git
    cd devto-blog-scraper
    ```

2. Install the required Python packages from the requirements.txt file:
    ```sh
    pip install -r requirements.txt
    ```

3. Download the Chrome WebDriver and ensure it is in your system's PATH.


4. Run the script to start scraping articles from Dev.to:
    ```sh
    python devtoblog.py
    ```

## Installing and running on docker

1. Build the Docker image:
    ```sh
    docker build -t devto_blog .
    ```

2. Run the Docker image:
    ```sh
    docker run devto_blog
    ```

## Edits to Increase OR Decrease the Output

If you want to maximize the output or the data extracted, you need to modify the `max_pages` parameter in the `get_all_articles()` function. This parameter controls the number of pages to scrape. By default, it is set to 10,000, but you can adjust it to your needs.


Steps to Increase the Output:
1. Locate the Function: Find the `get_all_articles()` function in your code.

2. Adjust the max_pages Parameter: Change the max_pages parameter to the desired number of pages you want to scrape. For example, to scrape 650 pages, set `max_pages=650`.

3. Run the Code or re-build your Dockerfile: Execute the script to start scraping the specified number of pages.

Example:
--------
To scrape 2,000 pages, you would modify the function call as follows:

```python
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

df_articles = get_all_articles(max_pages=2000)  
print(df_articles)
```

By increasing the max_pages parameter, you can extract more data, but keep in mind that scraping a large number of pages may take a significant amount of time and could put a load on the server. Always be considerate and follow the website's scraping policies.