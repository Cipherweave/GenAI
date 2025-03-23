import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

#########################################################
#
#  FUNCTION NAME CHANGED INTO get_legal_urls(wbesite_url)
#
##########################################################

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_legal_urls(website_url):
    prompt = f"""
Provide the terms and conditions and privacy policy URLs for the given domain name: {website_url}.

Your response must adhere to the following strict guidelines to prevent errors and ensure accuracy:

1. **Domain Verification**: Confirm that the provided domain name is a valid, publicly accessible website.

2. **Direct vs. Indirect:**
   - If the terms and conditions and privacy policy are found directly on the given domain, provide those URLs. Set the `"direct"` key in the JSON response to `true`.
   - If the given domain redirects to or is a subsidiary of a parent company (e.g., a product page on a company's main website), locate the terms and conditions and privacy policy on the parent company's site. Provide those URLs and set the `"direct"` key in the JSON response to `false`.
   - If you find that the domain is owned by a parent company, mention the **parent company** in the response.

3. **URL Accuracy**: Verify that the URLs provided are valid and lead directly to the terms and conditions and privacy policy pages.

4. **Error Handling**:
   - If the terms and conditions or privacy policy cannot be found, set the corresponding key's value to `false`.
   - If the domain is invalid or does not exist, return:
     ```json
     {{
       "terms_and_conditions": false,
       "privacy_policy": false,
       "direct": false
     }}
     ```

5. **Strict JSON Format**: The response MUST be in the following format:
   ```json
   {{
     "terms_and_conditions": "<URL or false>",
     "privacy_policy": "<URL or false>",
     "direct": <true or false>
   }}
    ```
"""
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    response = model.generate_content(prompt)
    json_text = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(json_text)
    


if __name__ == "__main__":
    website_url = 'https://www.harriscomputer.com/'
    legal_urls = get_legal_urls(website_url)
    print(legal_urls)