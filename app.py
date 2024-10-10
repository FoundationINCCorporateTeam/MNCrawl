import requests
from bs4 import BeautifulSoup
import json
import re

# Pre-defined categories with sample keywords
CATEGORIES = {
    'adult': ['porn', 'sex', 'xxx', 'adult', 'erotic'],
    'education': ['learning', 'school', 'university', 'science', 'research'],
    'games': ['game', 'play', 'video game', 'multiplayer', 'esports'],
    'news': ['news', 'breaking news', 'headline', 'journalism'],
    'shopping': ['buy', 'sale', 'shop', 'ecommerce', 'discount'],
    'sports': ['sports', 'football', 'basketball', 'cricket', 'soccer'],
    # Add up to 50-60 more categories
    # You can customize based on more specific genres.
}

# Function to fetch webpage content
def fetch_page(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    return None

# Function to extract all links from a webpage
def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('http'):
            links.add(href)
    return links

# Function to categorize website content based on keywords
def categorize_content(text):
    text = text.lower()  # Normalize text to lowercase
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if re.search(r'\b' + keyword + r'\b', text):
                return category
    return 'uncategorized'  # Default if no keywords match

# Function to crawl a website and categorize it
def crawl_and_categorize(start_url, max_pages=10):
    to_visit = [start_url]  # URLs to visit
    visited = set()         # Track visited URLs
    results = []            # Store results
    
    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        
        print(f"Crawling: {url}")
        html = fetch_page(url)
        if html:
            # Categorize the content
            category = categorize_content(html)
            print(f"Categorized as: {category}")
            
            # Store result
            results.append({'url': url, 'category': category})
            
            # Extract new links and add to visit list
            links = extract_links(html)
            to_visit.extend(links - visited)  # Avoid revisiting same URLs
        
        visited.add(url)
    
    return results

# Main function
def main(start_url):
    categorized_data = crawl_and_categorize(start_url, max_pages=50)
    
    # Save results to a JSON file
    with open('categorized_websites.json', 'w') as f:
        json.dump(categorized_data, f, indent=4)
    
    print("Results saved to categorized_websites.json")

# Example usage
if __name__ == "__main__":
    # Start with a seed URL
    start_url = 'http://example.com'
    main(start_url)
