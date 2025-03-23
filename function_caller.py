from privacy_policy_checker import policy_check
from policy_finder import get_privacy_policy_url
from web_suggester import search_related_websites
from web_security_checker import security_check
from privacy_policy_score import set_scale




def get_sentiment(web_name, url) -> list:
    lst = []
    policy_url = get_privacy_policy_url(url)
    print(policy_url)
    sentiment_lst = policy_check(policy_url)
    if len(sentiment_lst) == 2:
        search_related_websites(web_name)
    sentiment_lst.append(set_scale(sentiment_lst))
    security_lst = security_check(url)
    lst.append(sentiment_lst)
    lst.append(security_lst)
    
    return lst



if __name__ == "__main__":
    lst = get_sentiment("Harris Computers", "https://www.ali-rahbar.com/")
    print(lst)


