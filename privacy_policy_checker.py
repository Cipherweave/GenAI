from openai import OpenAI
from bs4 import BeautifulSoup
import requests


client = OpenAI(api_key="") 
ASSISTANT_ID = "asst_v2se6YGN5d3xm4voj2k8eMOb"

def extract_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract headings and paragraphs
    texts = []
    for tag in soup.find_all(["h1", "h2", "h3", "p"]):
        texts.append(tag.get_text(strip=True))  # Remove extra spaces

    return "\n".join(texts)  # Combine into a readable format



def policy_check(url):
    lst = []
    text = extract_text(url)
    thread = client.beta.threads.create()

    # Send the URL as a message to the assistant
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=text
    )

    # Run the assistant on the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    # Wait for the assistant to respond
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    # Retrieve the assistant's response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_response = messages.data[0].content[0].text.value

    lst.append(assistant_response)

    if assistant_response == "Policy Safe!":
        return lst
   
    # Send the URL as a message to the assistant
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Elaborate with quote"
    )

    # Run the assistant on the thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    # Wait for the assistant to respond
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    # Retrieve the assistant's response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_response = messages.data[0].content[0].text.value

    lst.append(assistant_response)

    return lst



if __name__ == "__main__":
    # Example usage
    url = "https://www.harriscomputer.com/privacy-policy"
    response = policy_check(url)
    print(response[0])
    lines = response[0].splitlines()
    print(lines)
    print("")
    if len(response) == 2:
        print(response[1])


