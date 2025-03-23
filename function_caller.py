from privacy_policy_checker import policy_check
from policy_finder import get_privacy_policy_url
from web_suggester import search_related_websites

def get_sentiment(web_name, url) -> list:
    policy_url = get_privacy_policy_url(url)
    sentiment_lst = policy_check(policy_url)
    if len(sentiment_lst) == 2:
        search_related_websites(web_name)
    return sentiment_lst

if __name__ == "__main__":
    lst = get_sentiment("Harris Computers", "https://www.harriscomputer.com/")
    print("here")
    print(lst)