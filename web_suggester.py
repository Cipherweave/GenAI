import cohere
import json
import os
from dotenv import load_dotenv
from duckduckgo_search import DDGS

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))


def get_related_websites(company_name: str) -> list:

    prompt = (f"Provide a list of exactly three websites or apps that are similar to {company_name}."  
            f' Rules: '
              f'- Only return the names of the websites or apps. '
              f'- No explanations, descriptions, or extra words.  '
              f'- The response must contain exactly three names.'
              f'- Do not include unrelated websites.  ')

    response = co.generate(
        model="command",
        prompt = prompt,
        max_tokens=50,
        temperature=0.5
        )

    suggestions = response.generations[0].text.strip()

    if "," in suggestions:
        lst = [s.strip() for s in suggestions.split(",")]
    else:
        lst = [s.strip() for s in suggestions.split("\n")]

    if len(lst) < 3:
        lst.extend(["Unknown"] * (3 - len(lst)))

    return lst[:3]


def get_official_urls(company_names):
    urls = {}

    with DDGS() as ddgs:
        for company in company_names:
            query = (f"{company} official site")
            search_results = ddgs.text(query, max_results=1)

            if search_results:
                urls[company] = search_results[0]["href"]

            else:
                urls[company] = "URL not found"

    return urls


def search_related_websites(company_name):

    related_websites = get_related_websites(company_name)

    official_urls = get_official_urls(related_websites)

    final_result = {"company": company_name, "related_companies": official_urls}

    with open("related_companies_urls.json", "w") as json_file:
        json.dump(final_result, json_file, indent = 4)

    return final_result


if __name__ == '__main__':
    print(search_related_websites('google'))

