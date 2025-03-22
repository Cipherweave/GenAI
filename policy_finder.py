import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_privacy_policy_url(website_url):
    try:
        response = requests.get(website_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for links that might has privacy policy url
        links = soup.find_all(["h1", "h2", "h3", "p", "a","span", "button", "div"], href=True)
        for link in links:
            href = link['href']
            text = link.text.lower()

            # Check both href and link text for privacy-related terms
            if 'privacy' in href.lower() or 'privacy' in text:
                # join URLs using urljoin
                absolute_url = urljoin(website_url, href)
                return absolute_url
        return None
    except Exception as e:
        print(f"Error fetching privacy policy: {e}")
        return None

if __name__ == "__main__":
    website_url = 'https://www.harriscomputer.com/'
    privacy_url = get_privacy_policy_url(website_url)
    if privacy_url:
        print(f"Privacy Policy URL: {privacy_url}")
    else:
        print("Privacy policy URL not found.")
