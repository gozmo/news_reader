import feedparser
from src.entry import Entry
from tqdm import tqdm

def latest():
    url = "http://rss.slashdot.org/Slashdot/slashdotMain"
    posts = feedparser.parse(url)

    articles = []
    for post in tqdm(posts["entries"], desc="slashdot"):
        article = Entry(text = post["title"], 
                        target_link = post["links"][0]["href"],
                        source_link = post["link"],
                        source_page="slashdot")
        articles.append(article)
    return articles
