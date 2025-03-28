from privacy_policy_checker import policy_check
import cohere
from dotenv import load_dotenv
import os
import json


load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))


def set_scale(lst):
    
    prompt = (f"The following list contains problems in a website's privacy policy: {lst[0]}. "
          f"Based on these issues, assign a trust score from 1 to 10. "
          f"A higher number means the website is more trustworthy, while a lower number "
          f"means it's less trustworthy."
            f"if {lst[0]} is policy safe then give a score of 10. "
              f"Else decrease the score based on the problems."
          f"Return only a single integer between 1 and 10, nothing else."
        f"Do nor return any text just a single integer")



    response = co.generate(
        model = "command",
        prompt = prompt,
        max_tokens = 2,
        temperature = 0.0,
        k = 0,
        stop_sequences = ["\n"]
    )

    ai_response = response.generations[0].text.strip()

    try:
        score = int(ai_response)
        if 1 <= score <= 10:
            return score

    except ValueError:
        pass

    return -1


def main(lst):

    output = policy_check(lst)
    rate = set_scale(output)
    result = {"trust_score": rate}

    return json.dumps(result, indent=4)

if __name__ == '__main__':

    url = "https://www.ali-rahbar.com"
    print(main(url))
