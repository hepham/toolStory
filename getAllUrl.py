import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_all_urls(base_url):
    # Send a GET request to the URL
    response = requests.get(base_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all the anchor (a) tags
        all_links = soup.find_all('a')

        # Extract URLs from href attributes
        urls = [link.get('href') for link in all_links if link.get('href')]

        # Convert relative URLs to absolute URLs
        urls = [urljoin(base_url, url) for url in urls]

        # Filter out external URLs if needed
        domain = urlparse(base_url).netloc
        urls = [url for url in urls if urlparse(url).netloc == domain]

        return urls
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

# Example usage:
base_url = "https://truyenvipvip.com/"
all_urls = get_all_urls(base_url)

# Print or process the extracted URLs
for url in all_urls:
    print(url)