from src.dataset import TrainingDataset
from src.dataset import ClassificationDataset
from src.bert import Bert
from src.constants import Labels
from src.feeds import hackernews
from src.feeds import reddit
from src.feeds import slashdot
from src.feeds import hackernoon
from src.feeds import medium

from tqdm import tqdm
import pudb
from src import io_utils
import webbrowser


def list_articles():
    latest_articles = io_utils.read_label(Labels.LATEST)
    latest_articles = sorted(latest_articles, key=lambda x:x.score, reverse=True)
    return latest_articles

def update():
    hn_articles = hackernews.latest()
    rd_articles = reddit.latest()
    slashdot_articles = slashdot.latest()
    hackernoon_articles = hackernoon.latest()
    medium_articles = medium.latest()

    articles = hn_articles + rd_articles + hackernoon_articles + slashdot_articles + medium_articles
    dataset = ClassificationDataset(articles)

    bert = Bert()
    bert.load()
    classifications = bert.classify(dataset)

    io_utils.clear_label(Labels.LATEST)
    for score, article in zip(classifications, articles):
        article.set_score(score[0])
        if not (io_utils.in_label(Labels.POSITIVE, article) or \
                io_utils.in_label(Labels.NEGATIVE, article) or \
                io_utils.in_label(Labels.UNLABELED, article)):
            io_utils.append(Labels.LATEST, article)
            io_utils.append(Labels.UNLABELED, article)

def annotate(indices, label):
    articles = list_articles()
    articles_to_annotate = [articles[idx] for idx in indices]

    for article in articles_to_annotate:
        if label == Labels.POSITIVE or label == Labels.NEGATIVE:
            io_utils.remove(Labels.LATEST, article)
            io_utils.remove(Labels.UNLABELED, article)

        io_utils.append(label, article)

def open(numbers):
    for number in numbers:
        articles = list_articles()
        article = articles[number]
        webbrowser.open(article.target_link)
    annotate(numbers, Labels.POSITIVE)

def train():
    dataset = TrainingDataset()

    bert = Bert()
    bert.train(dataset)
    bert.save()

def update_scores():
    bert = Bert()
    bert.load()
    for label in [Labels.LATEST, Labels.POSITIVE, Labels.NEGATIVE, Labels.UNLABELED]:
        articles = io_utils.read_label(label)

        dataset = ClassificationDataset(articles)
        classifications = bert.classify(dataset)

        io_utils.clear_label(label)
        for score, article in zip(classifications, articles):
            article.score = score[0]
            io_utils.append(label, article)

def unlabeled():
    articles = io_utils.read_label(Labels.UNLABELED)
    articles = sorted(articles, key=lambda x:x.score, reverse=True)
    return articles

