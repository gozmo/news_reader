
import feedparser
from src.entry import Entry
from tqdm import tqdm

def latest():
    articles = []
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
    for subreddit in tqdm(subreddits, desc="reddit"):

        url = f"https://www.reddit.com/r/{subreddit}/.rss"

        posts = feedparser.parse(url)

        for post in posts["entries"]:
            article = Entry(text = post["title"], 
                            target_link = post["links"][0]["href"],
                            source_link = post["link"],
                            source_page =f"reddit-{subreddit}")
            articles.append(article)
    return articles
