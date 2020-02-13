from datetime import datetime
from src import constants
from src import io_utils
from src.entry import Entry
from time import mktime
from tqdm import tqdm
from twitter import OAuth
from twitter import Twitter
import dateutil.parser
import feedparser
import pytz

def get_news():
    sources = [("hackernews", "https://news.ycombinator.com/rss"),
               ("slashdot", "http://rss.slashdot.org/Slashdot/slashdotMain")]
    #https://www.microsoft.com/en-us/research/blog/
    #https://ai.facebook.com/blog/
    # https://openai.com/blog/
    #https://deepmind.com/blog 
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

    sources.extend(reddit)
    sources.extend(medium)
    sources.extend(hackernoon)


    articles = []
    for source, url in tqdm(sources, desc="Feeds"):
        posts = feedparser.parse(url)
        for post in posts["entries"]:
            dt = datetime.fromtimestamp(mktime(post["updated_parsed"]))
            dt = pytz.utc.localize(dt)
            article = Entry(text = post["title"], 
                            link = post["links"][0]["href"],
                            publish_time = dt,
                            source=source)
            articles.append(article)
    return articles


def get_twitter():
    consumer_token = io_utils.read_file(constants.Twitter.CONSUMER_TOKEN)
    consumer_secret = io_utils.read_file(constants.Twitter.CONSUMER_SECRET)
    access_token = io_utils.read_file(constants.Twitter.ACCESS_TOKEN)
    access_secret = io_utils.read_file(constants.Twitter.ACCESS_SECRET)
    oauth = OAuth(access_token, access_secret, consumer_token, consumer_secret)
    t = Twitter(auth=oauth)
    timeline = t.statuses.home_timeline()
    articles = []
    for post in timeline:
        time = dateutil.parser.parse(post["created_at"])

        article = Entry(text = post["text"], 
                        link = post["user"]["url"],
                        publish_time = time,
                        source= post["user"]["name"])
        articles.append(article)
    return articles

