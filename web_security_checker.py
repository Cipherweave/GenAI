from bs4 import BeautifulSoup
import requests
from openai import OpenAI


client = OpenAI(api_key="") 
ASSISTANT_ID = "asst_vZcbERUnnB1DGgz7ase0EZig"


def extract_important_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract important elements
        important_elements = []
        
        # Extract all links
        for link in soup.find_all("a", href=True):
            important_elements.append(str(link))
        
        # Extract all forms and input fields
        for form in soup.find_all("form"):
            important_elements.append(str(form))
        
        # Extract all script tags
        for script in soup.find_all("script"):
            important_elements.append(str(script))
        
        # Extract meta refresh (redirects)
        for meta in soup.find_all("meta", attrs={"http-equiv": "refresh"}):
            important_elements.append(str(meta))
        
        # Extract hidden elements safely
        for hidden in soup.find_all(style=lambda value: value and isinstance(value, str) and ("display:none" in value.lower() or "opacity:0" in value.lower())):
            important_elements.append(str(hidden))
        
        return "\n".join(important_elements) 
    
    except Exception as e:
        return f"Error: {e}"
    

def security_check(url: str):
    lst = []
    text = extract_important_html(url)
    thread = client.beta.threads.create()

    print(text)

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
    
    print("here")

    # Retrieve the assistant's response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_response = messages.data[0].content[0].text.value

    lst.append(assistant_response)

    if assistant_response == "Security Safe!":
        return lst
   
    # Send the URL as a message to the assistant
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="Elaborate"
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
    # s = extract_important_html("https://www.harriscomputer.com/")
    # print(s)
    lst = security_check("https://www.harriscomputer.com/")
    print(lst[0])
    lines = lst[0].splitlines()
    print(lines)
    print("")
    if len(lst) == 2:
        print(lst[1])
    