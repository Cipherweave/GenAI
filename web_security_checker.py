from bs4 import BeautifulSoup
import requests
from openai import OpenAI
<<<<<<< HEAD
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
<<<<<<< HEAD
=======
from dotenv import load_dotenv
import os
>>>>>>> c432317 (Final)
=======
from dotenv import load_dotenv
import os
>>>>>>> 955d285 (Back-end version 2)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ASSISTANT_ID = "asst_vZcbERUnnB1DGgz7ase0EZig"


# Returns a list of 3 values
def extract_important_html(url) -> str:
    try:
        # response = requests.get(url)
        # response.raise_for_status()  # Raise an error for bad responses
        
        # soup = BeautifulSoup(response.text, "html.parser")
        
        # # Extract important elements
        important_elements = []
        
        # # Extract all links
        # for link in soup.find_all("a", href=True):
        #     important_elements.append(str(link))
        
        # # Extract all forms and input fields
        # for form in soup.find_all("form"):
        #     important_elements.append(str(form))
        
        # # Extract all script tags
        # for script in soup.find_all("script"):
        #     important_elements.append(str(script))
        
        # # Extract meta refresh (redirects)
        # for meta in soup.find_all("meta", attrs={"http-equiv": "refresh"}):
        #     important_elements.append(str(meta))
        
        # # Extract hidden elements safely
        # for hidden in soup.find_all(style=lambda value: value and isinstance(value, str) and ("display:none" in value.lower() or "opacity:0" in value.lower())):
        #     important_elements.append(str(hidden))
        
        # if not important_elements:
        options = Options()
        options.add_argument("--headless")  # Headless mode
        options.add_argument("--disable-gpu")  # Prevents GPU-related issues
        options.add_argument("--no-sandbox")  # Helps in restricted environments
        options.add_argument("--window-size=1920,1080")  # Ensures full page loading
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.implicitly_wait(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.quit()

        for hidden in soup.find_all(style=lambda v: v and ("display:none" in v.lower() or "opacity:0" in v.lower())):
            important_elements.append(str(hidden))

        for tag in soup.find_all(["a", "form", "script", "meta"]):
            content = str(tag)
            if len(content) > 500: 
                continue
            important_elements.append(content)

        return "\n".join(important_elements) 
    
    except Exception as e:
        return f"Error: {e}"
    


    

def security_check(url: str):
    lst = []
    text = extract_important_html(url)
    thread = client.beta.threads.create()

<<<<<<< HEAD
    text = text[0: 60000]
=======
>>>>>>> c432317 (Final)

   
    
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
<<<<<<< HEAD


=======
    
>>>>>>> c432317 (Final)

    # Retrieve the assistant's response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_response = messages.data[0].content[0].text.value
   
   

    lst.append(assistant_response)

    if assistant_response == "Security Safe!":
        lst.append("")
        lst.append("Safe")
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

    # Send the URL as a message to the assistant
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="How is the safety"
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
<<<<<<< HEAD
    lst = security_check("https://privacycenter.instagram.com/policy")
    print(lst[0])
    print(lst[1])
    print(lst[2])
=======
    lst = security_check("http://henryyuen.net/")
    print(lst[0])
    lines = lst[0].splitlines()
    print(lines)
    if len(lst) == 2:
        print(lst[1])
>>>>>>> c432317 (Final)
    