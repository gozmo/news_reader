import jsonlines
import json
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

def clear_label(label):
    path = get_label_path(label)
    with open(path, "w") as f:
        f.write("")

def in_label(source, label, article):
    articles = read_label(source, label)
    return article in articles

def append(label, article):
    articles = read_label(label)
    if article in articles:
        return

    target = get_label_path(label)
    with jsonlines.open(target, "a") as writer:
        writer.write(article.to_dict())

def remove(label, article_to_remove):
    target = get_label_path(label)
    articles = []
    with jsonlines.open(target) as reader:
        for elem in reader:
            article = Entry(**elem)
            if article != article_to_remove:
                articles.append(article)

    clear_label(label)
    with jsonlines.open(target, "a") as writer:
        for article in articles:
            writer.write(article.to_dict())
