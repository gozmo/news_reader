from src.dataset import TrainingDataset
from src.dataset import ClassificationDataset
from src.transformer import Bert
from src.constants import Labels
from src.constants import Sources
from src.constants import FFN_MODEL_NAME
from src.constants import TRANSFORMER_MODEL_NAME
from src.constants import BASE_PATH
from src.feeds import get_news
from src.feeds import get_twitter

from tqdm import tqdm
import pudb
from src import io_utils
import webbrowser
import datetime
from dateutil import parser



def list_articles(source, label):
    articles = io_utils.read_label(source, label)
    if source == Sources.BLOGS:
        articles = sorted(latest_articles, key=lambda x:x.publish_time, reverse=True)
    else:
        articles = sorted(latest_articles, key=lambda x:x.score, reverse=True)
    return articles

def update(source):
    if source == Source.NEWS:
        entities = get_news()
        classify = True 
    elif source == Source.TWITTER:
        entities = get_twitter()
        classify = True
    elif source == source.BLOGS:
        entities ==get_blogs()
        classify = False

    if classify:
        transformer_path = f"{BASE_PATH}/{source}/{TRANSFORMER_MODEL_NAME}"
        ffn_path = f"{BASE_PATH}/{source}/{FFN_MODEL_NAME}"
        transformer = transformer()
        transformer.load(transformer_path, ffn_path)

        dataset = ClassificationDataset(entities)
        classifications = transformer.classify(dataset)
        for score, entity in zip(classifications, entites):
            entity.set_score(score[0])


    for entity in entites:
        if not (io_utils.in_label(source, Labels.POSITIVE, entity) or \
                io_utils.in_label(source, Labels.NEGATIVE, entity) or \
                io_utils.in_label(source, Labels.UNLABELED, entity)):
            io_utils.append(source, Labels.LATEST, entity)
            io_utils.append(source, Labels.UNLABELED, entity)

    io_utils.remove_old_entites(source, Labels.LATEST, datetime.time(hour=24))

def annotate(source, indices, label):
    articles = list_articles(source, label)
    articles_to_annotate = [articles[idx] for idx in indices]

    for article in articles_to_annotate:
        if label == Labels.POSITIVE or label == Labels.NEGATIVE:
            io_utils.remove(source, Labels.LATEST, article)
            io_utils.remove(source, Labels.UNLABELED, article)

        io_utils.append(source, label, article)

def open(source, label, numbers):
    for number in numbers:
        articles = list_articles(source, label)
        article = articles[number]
        webbrowser.open(article.target_link)
    annotate(numbers, Labels.POSITIVE)

def train(source):
    dataset = TrainingDataset()

    bert = Bert()
    bert.train(dataset)
    bert.save()

def update_scores(source):
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

def unlabeled(source):
    articles = io_utils.read_label(Labels.UNLABELED)
    articles = sorted(articles, key=lambda x:x.score, reverse=True)
    return articles

