import jsonlines
import json
import datetime
from src.constants import Labels
from src.constants import BASE_PATH
from src.entry import Entry 

def get_label_path(source, label):
    return f"{BASE_PATH}/{source}/{label}"

def read_label(source, label):
    target = get_label_path(source, label)

    articles = []
    with jsonlines.open(target) as reader:
        for elem in reader:
            article = Entry(**elem)
            articles.append(article)

    return articles

def clear_label(source, label):
    path = get_label_path(source, label)
    with open(path, "w") as f:
        f.write("")

def in_label(source, label, article):
    articles = read_label(source, label)
    return article in articles

def append(source, label, article):
    articles = read_label(source, label)
    if article in articles:
        return

    target = get_label_path(source, label)
    with jsonlines.open(target, "a") as writer:
        writer.write(article.to_dict())

def remove(source, label, article_to_remove):
    target = get_label_path(source, label)
    articles = []
    with jsonlines.open(target) as reader:
        for elem in reader:
            article = Entry(**elem)
            if article != article_to_remove:
                articles.append(article)

    clear_label(source, label)
    with jsonlines.open(target, "a") as writer:
        for article in articles:
            writer.write(article.to_dict())

def remove_old_entries(source, label, time_limit):
    articles = read_label(source, label)
    now = datetime.datetime.now(datetime.timezone.utc)
    for article in articles:
        if time_limit < now - article.publish_time:
            remove(source, label, article)

def read_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    return content.strip()
