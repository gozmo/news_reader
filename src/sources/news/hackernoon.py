
import feedparser
from src.entry import Entry
from tqdm import tqdm

def latest():
    tags = [ "ai", "amazon", "apple", "big-data", "bitcoin", "blockchain",
            "coding", "cryptocurrency", "cybersecurity", "data-science", "deep-learning",
            "economics", "engineering", "facebook", "funding", "future", "futurist",
            "google", "machine-learning", "marketing", "pitching", "privacy", "programming",
            "robotics", "scaling", "software-development", "space", "startup-advice", "startups",
            "technology-trends", "virtual-reality", "wtf"]

    articles = []
    # for tag in tqdm(tags, desc="hackernoon"):
        # url = f"https://hackernoon.com/tagged/{tag}/feed"
        # posts = feedparser.parse(url)
        # for post in posts["entries"]:
            # article = Entry(text = post["title"], 
                            # target_link = post["links"][0]["href"],
                            # source_link = post["links"][0]["href"],
                            # source_page=f"hackernoon-{tag}")
            # articles.append(article)
    url = f"https://hackernoon.com/feed"
    posts = feedparser.parse(url)
    for post in tqdm(posts["entries"], desc="hackernoon", leave=False):
        article = Entry(text = post["title"], 
                        target_link = post["links"][0]["href"],
                        source_link = post["links"][0]["href"],
                        source_page=f"hackernoon")
        articles.append(article)
    print("Hackernoon ✔") 
    return articles
