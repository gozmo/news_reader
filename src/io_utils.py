import jsonlines
from src.constants import Paths
from src.constants import Labels
from src.entry import Entry 

def get_label_path(label):
    if label == Labels.POSITIVE:
        return Paths.POSITIVE
    elif label == Labels.NEGATIVE:
        return Paths.NEGATIVE
    elif label == Labels.LATEST:
        return Paths.LATEST
    elif label == Labels.UNLABELED:
        return Paths.UNLABELED

def read_label(label):
    target = get_label_path(label)

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

def in_label(label, article):
    articles = read_label(label)
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
