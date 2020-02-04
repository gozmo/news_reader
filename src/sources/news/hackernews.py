import feedparser
from src.entry import Entry
from tqdm import tqdm

def latest():
    url = "https://news.ycombinator.com/rss"
    posts = feedparser.parse(url)

    articles = []
    for post in tqdm(posts["entries"], desc="hackernews", leave=False):
        article = Entry(text = post["title"], 
                        target_link = post["links"][0]["href"],
                        source_link = post["comments"],
                        source_page="hackernews")
        articles.append(article)
        print("Hackernews ✔") 
    return articles
