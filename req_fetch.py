from articlextract import ContentExtractor
import requests 


def get_resonse(url):
    
    res = requests.get(url)
    if res.status_code != 200:
        raise f"Http error {res.status_code}"
    
    return res.text
    
    
def extrcat_data(url):
    try:
        html = get_resonse(url)
        article_data = ContentExtractor(html,url).extract()
    except Exception as e:
        print(str(e))
    return article_data
        
    
    
if __name__ == "__main__":
    url = "https://www.dailyrecord.co.uk/news/scottish-news/low-level-platforms-closed-glasgow-36788196"
    data = extrcat_data(url=url)
    print(data)