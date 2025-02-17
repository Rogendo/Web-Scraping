import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
BASE_WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/"
BATCH_SIZE = 300  # Number of articles to scrape per batch
TOTAL_ARTICLES_PER_TOPIC = 10000  # Total number of articles to scrape per topic
DELAY = 1  # Delay between requests (in seconds)

def load_topics(file_path):
    """
    Load topics from a text file, one topic per line.
    Returns a list of topics.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            topics = [line.strip() for line in f if line.strip()]
            return topics
    except Exception as e:
        print(f"Error loading topics from {file_path}: {e}")
        return []

# Default finance topics (will be used if no topics file is found)
default_finance_topics = [
"Finance",
"Banking",
"Investment",
"Stock Market",
"Bonds",
"Equities",
"Mutual Funds",
"Hedge Funds",
"Portfolio Management",
"Financial Analysis",
"Corporate Finance",
"personal Finance",
"Financial Planning"
]

# load topics from a text file; if not found, use the default list.
topics_file = "./finance.txt"
if os.path.exists(topics_file):
    TOPICS = load_topics(topics_file)
    if not TOPICS:
        print("No topics loaded from file; using default finance topics.")
        TOPICS = default_finance_topics
else:
    print(f"{topics_file} not found. Using default finance topics.")
    TOPICS = default_finance_topics

# Function to search Wikipedia for relevant articles using the Wikipedia API
def search_wikipedia_articles(query, num_results, offset=0):
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "utf8": 1,
        "srlimit": num_results,
        "sroffset": offset
    }
    response = requests.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()
    
    if "query" not in data or "search" not in data["query"]:
        print(f"Error: No results found for '{query}'.")
        return []
    
    articles = [
        {
            "title": result["title"],
            "url": BASE_WIKIPEDIA_URL + result["title"].replace(" ", "_")
        }
        for result in data["query"]["search"]
    ]
    return articles

# Function to scrape a single Wikipedia page
def scrape_wikipedia_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title_tag = soup.find('h1', {'id': 'firstHeading'})
        title = title_tag.text.strip() if title_tag else "No title found"

        # Extract summary (first 2 paragraphs)
        summary_div = soup.find('div', {'class': 'mw-parser-output'})
        if summary_div:
            summary_paragraphs = summary_div.find_all('p', recursive=False)[:2]  # First 2 paragraphs
            summary = "\n".join([p.get_text(strip=True) for p in summary_paragraphs])
        else:
            summary = "No summary available."

        # Extract the entire content
        full_content = []
        if summary_div:
            for element in summary_div.find_all(['p', 'h2', 'h3', 'ul', 'ol']):
                if element.name in ['h2', 'h3']:
                    full_content.append(f"\n=== {element.get_text(strip=True)} ===\n")  # Add headers with separators
                elif element.name in ['ul', 'ol']:
                    full_content.append("\n".join([li.get_text(strip=True) for li in element.find_all('li')]))
                else:
                    # Remove references (<sup>) and other non-content elements
                    for sup in element.find_all('sup'):
                        sup.decompose()
                    full_content.append(element.get_text(strip=True))
        full_content = "\n".join(full_content)

        # Extract internal links (related articles)
        links = []
        if summary_div:
            links = [a['href'] for a in summary_div.find_all('a', href=True) if '/wiki/' in a['href']]
            links = list(set(links))  # Remove duplicates

        return {
            "title": title,
            "summary": summary,
            "content": full_content,
            "links": links
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Main function to scrape multiple pages in batches for a specific topic
def scrape_topic_content(topic):
    print(f"Searching for '{topic}' articles...")
    all_data = []
    offset = 0

    while len(all_data) < TOTAL_ARTICLES_PER_TOPIC:
        print(f"Fetching batch starting at offset {offset} for topic '{topic}'...")
        articles = search_wikipedia_articles(topic, BATCH_SIZE, offset)
        if not articles:
            print(f"No more articles found for '{topic}'. Exiting batch loop.")
            break

        print(f"Found {len(articles)} articles. Starting scraping...")
        for i, article in enumerate(articles, start=1):
            print(f"Scraping article {i}/{len(articles)}: {article['title']}")
            scraped_data = scrape_wikipedia_page(article['url'])
            if scraped_data:
                scraped_data["url"] = article['url']
                all_data.append(scraped_data)
            time.sleep(DELAY)  # Respectful delay between requests

            # Stop if we've reached the total number of articles
            if len(all_data) >= TOTAL_ARTICLES_PER_TOPIC:
                break

        offset += BATCH_SIZE  # Move to the next batch

    return all_data

# Save data to a CSV file
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Run the scraper for all topics
if __name__ == "__main__":
    for topic in TOPICS:
        print(f"\nStarting the scraper for topic: {topic}...")
        scraped_data = scrape_topic_content(topic)
        if scraped_data:
            csv_filename = f"{topic.replace(' ', '_').lower()}_data.csv"
            save_to_csv(scraped_data, csv_filename)
