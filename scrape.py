import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


def scrape_url(url):
    try:
        response = requests.get(url, timeout=2)  # Set a timeout (in seconds) for the request
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text()
            return text_content
        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error while scraping {url}: {e}")
        return None


def scrape_from_file(file_path):
    scraped_data = []

    with open(file_path, 'r') as file:
        urls = file.read().split(',')
        for idx, url in enumerate(urls):
            text_content = scrape_url(url)
            if text_content:
                scraped_data.append({'URL': url, 'Data': text_content})
            time.sleep(2)  # Add a delay to avoid being blocked

    return scraped_data


def create_dashboard(scraped_data):
    df = pd.DataFrame(scraped_data)
    df.to_csv('scraped_data.csv', mode='a', header=False, index=False)
    print(f"Data appended to scraped_data.csv")


if __name__ == "__main__":
    file_path = "100 website scraper"  # Update the file path based on your location
    scraped_data = scrape_from_file(file_path)

    if scraped_data:
        create_dashboard(scraped_data)
