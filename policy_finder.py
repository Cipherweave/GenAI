import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

#########################################################
#
#  FUNCTION NAME CHANGED INTO get_legal_urls(wbesite_url)
#
##########################################################

def find_link_and_text(element):
    """Helper function to find href and combined text from an element and its parents"""
    # Get href from current element or nearest parent
    href = None
    current = element
    while current and not href:
        href = current.get('href')
        current = current.parent
        # Stop if we reach the top or hit a new link
        if not current or current.name == 'a':
            break
    
    # Get all text from the element and its children
    text = ' '.join(element.stripped_strings).lower()
    return href, text

def get_legal_urls(website_url):
    try:
        response = requests.get(website_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        privacy_url = None
        terms_url = None
        
        # Find all relevant elements that might contain or be part of links
        elements = soup.find_all(['a', 'div', 'span', 'p', 'button'])
        
        for element in elements:
            href, text = find_link_and_text(element)
            if not href:
                continue
                
            # Create absolute URL
            absolute_url = urljoin(website_url, href)
            
            # Check for privacy policy
            if 'privacy' in href.lower() or 'privacy' in text:
                privacy_url = absolute_url
            
            # Check for terms and conditions
            terms_keywords = ['terms', 'conditions', 'terms of use', 'terms of service', 'tos']
            if any(keyword in href.lower() or keyword in text for keyword in terms_keywords):
                terms_url = absolute_url
                
            # If we found both, we can return early
            if privacy_url and terms_url:
                return {'privacy': privacy_url, 'terms': terms_url}
                
        return {'privacy': privacy_url, 'terms': terms_url}
    except Exception as e:
        print(f"Error fetching URLs: {e}")
        return {'privacy': None, 'terms': None}

if __name__ == "__main__":
    website_url = 'https://www.linkedin.com/feed/'
    legal_urls = get_legal_urls(website_url)
    
    if legal_urls['privacy']:
        print(f"Privacy Policy URL: {legal_urls['privacy']}")
    else:
        print("Privacy policy URL not found.")
        
    if legal_urls['terms']:
        print(f"Terms & Conditions URL: {legal_urls['terms']}")
    else:
        print("Terms & Conditions URL not found.")
