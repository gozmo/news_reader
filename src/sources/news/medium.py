import feedparser
from src.entry import Entry
from tqdm import tqdm

def latest():
    users = ["towardsdatascience"]

    articles = []
    for user in tqdm(users, desc="medium", leave=False):
        url = f"https://www.medium.com/feed/{user}"
        posts = feedparser.parse(url)
        for post in posts["entries"]:
            article = Entry(text = post["title"], 
                            target_link = post["links"][0]["href"],
                            source_link = post["links"][0]["href"],
                            source_page=f"medium-{user}")
            articles.append(article)

    print("Medium ✔") 
    return articles
