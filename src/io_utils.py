import jsonlines
from src.constants import Labels
from src.constants import BASE_PATH
from src.entry import Entry
import pytz

def get_label_path(source, label):
    return f"{BASE_PATH}/{source}/{label}.jsonl"

def read_label(source, label):
    target = get_label_path(source, label)

    articles = []
    with jsonlines.open(target) as reader:
        for elem in reader:
            article = Entry(**elem)
            try:
                article.publish_time = pytz.utc.localize(article.publish_time)
            except:
                pass
            articles.append(article)

    return articles

def write_label(source, label, articles):
    target = get_label_path(source, label)
    with jsonlines.open(target, "w") as writer:
        for article in articles:
            writer.write(article.to_dict())

def read_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    return content.strip()

