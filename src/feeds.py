import feedparser
import twitter
from src.entry import Entry
from tqdm import tqdm

def get_news():
    sources = [("hackernews", "https://news.ycombinator.com/rss"),
               ("slashdot", "http://rss.slashdot.org/Slashdot/slashdotMain")]

    subreddits = ["machinelearning", \
                  "python", \
                  "linux", \
                  "LanguageTechnology", \
                  "mlquestions", \
                  "deeplearning", \
                  "neuralnetworks", \
                  "programming", \
                  "datascience", \
                  "pytorch", \
                  "tensorflow", \
                  "vim", \
                  "tmux", \
                  "nlp", \
                  "statistics", \
                  "learningmachinelearning"]
    reddit = [(f"reddit {subreddit}", f"https://www.reddit.com/r/{subreddit}/.rss") for subreddit in subreddits]
    medium = [(f"medium {user}", f"https://www.medium.com/feed/{user}") for user in ["towardsdatascience"]]

    hn_tags = [ "ai", "amazon", "apple", "big-data", "bitcoin", "blockchain",
            "coding", "cryptocurrency", "cybersecurity", "data-science", "deep-learning",
            "economics", "engineering", "facebook", "funding", "future", "futurist",
            "google", "machine-learning", "marketing", "pitching", "privacy", "programming",
            "robotics", "scaling", "software-development", "space", "startup-advice", "startups",
            "technology-trends", "virtual-reality", "wtf"]
    hackernoon = [(f"hackernoon {tag}",  f"https://hackernoon.com/tagged/{tag}/feed") for tag in hn_tags] 

    # sources.extend(reddit)
    # sources.extend(medium)
    # sources.extend(hackernoon)


    articles = []
    for source, url in tqdm(sources, desc="News"):
        posts = feedparser.parse(url)
        for post in posts["entries"]:
            article = Entry(text = post["title"], 
                            link = post["links"][0]["href"],
                            publish_time = post["updated"],
                            source=source)
            articles.append(article)
    return articles

def get_twitter():
    pass
