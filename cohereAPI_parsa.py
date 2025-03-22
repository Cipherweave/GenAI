import cohere
import json
import os
from dotenv import load_dotenv
from duckduckgo_search import DDGS

load_dotenv()
cohere_api = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api)


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
        temperature=0.7
        )

    suggestions = response.generations[0].text.strip().split("\n")

    lst = []
    for s in suggestions:
        if s:
            lst.append(s)

        if len(lst) == 3:
            break

    return lst


def get_official_urls(company_names):
    urls = {}

    with DDGS() as ddgs:
        for company in company_names:
            query = (f"{company} official website, no account or log in page just"
                     f"the official website")
            search_results = ddgs.text(query, max_results=1)

            if search_results:
                urls[company] = search_results[0]["href"]

    return urls

def main(company_name):
    related_websites = get_related_websites(company_name)

    official_urls = get_official_urls(related_websites)

    final_result = {"company": company_name, "related_companies": official_urls}

    with open("related_companies_urls.json", "w") as json_file:
        json.dump(final_result, json_file, indent = 4)

    return final_result


if __name__ == '__main__':
    print(main('instagram'))

