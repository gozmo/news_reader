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
import webbrowser
import datetime
from dateutil import parser
from src.database import db

def list_articles(source, label, all_entries):
    articles = db.read(source, label)
    if source == Sources.BLOGS: 
        articles = sorted(articles, key=lambda x:x.publish_time, reverse=True)
    elif source == Sources.TWITTER:
        articles = sorted(articles, key=lambda x:x.score, reverse=True)
        if not all_entries:
            articles = [article for article in articles if article.score > 0.15]
    elif source == Sources.NEWS:
        articles = sorted(articles, key=lambda x:x.score, reverse=True)
    return articles

def update(source):
    if source == Sources.NEWS:
        entities = get_news()
        classify = True 
    elif source == Sources.TWITTER:
        entities = get_twitter()
        classify = True
    elif source == sources.BLOGS:
        entities ==get_blogs()
        classify = False

    if classify:
        transformer = Bert()
        transformer.load(source)

        dataset = ClassificationDataset(entities)
        classifications = transformer.classify(dataset)
        for score, entity in zip(classifications, entities):
            entity.set_score(score[0])


    for entity in tqdm(entities, desc="IO operations"):
        if not (entity in db.read(source, Labels.POSITIVE) or \
                entity in db.read(source, Labels.NEGATIVE) or \
                entity in db.read(source, Labels.UNLABELED)):
            db.append(source, Labels.LATEST, entity)
            db.append(source, Labels.UNLABELED, entity)

    
    now = datetime.datetime.now(datetime.timezone.utc)
    time_limit = datetime.timedelta(hours=24)

    for article in db.read(source, Labels.LATEST):
        if time_limit < now - article.publish_time:
            db.delete(source, Labels.LATEST, article)

    db.write()

def annotate(source, indices, label):
    articles = list_articles(source, Labels.LATEST, True)
    articles_to_annotate = [articles[idx] for idx in indices]

    for article in articles_to_annotate:
        if label == Labels.POSITIVE or label == Labels.NEGATIVE:
            db.delete(source, Labels.LATEST, article)
            db.delete(source, Labels.UNLABELED, article)

        db.append(source, label, article)

    db.write()

def open(source, numbers):
    for number in numbers:
        articles = list_articles(source, Labels.LATEST, True)
        article = articles[number]
        webbrowser.open(article.link)
    annotate(source, numbers, Labels.POSITIVE)


def train(source):
    dataset = TrainingDataset(source)

    bert = Bert()
    bert.train(dataset)
    bert.save(source)

def update_scores(source):
    bert = Bert()
    bert.load(source)
    for label in [Labels.LATEST, Labels.POSITIVE, Labels.NEGATIVE, Labels.UNLABELED]:
        articles = db.read(source, label)

        dataset = ClassificationDataset(articles)
        classifications = bert.classify(dataset)

        for score, article in zip(classifications, articles):
            article.score = score[0]
            db.update(source, label, article)
    db.write()

def unlabeled(source):
    articles = db.read(source, Labels.UNLABELED)
    articles = sorted(articles, key=lambda x:x.score, reverse=True)
    return articles

def init():
    for source in [Sources.TWITTER, Sources.NEWS, Sources.BLOGS]:
        path = f"{BASE_PATH}/{source}"
        os.makedirs(path, exist_ok=True)
        bert = Bert()
        bert.save(source)
        for label in [Labels.NEGATIVE, Labels.POSITIVE, Labels.LATEST, Labels.UNLABELED]:
            path = f"{BASE_PATH}/{source}/{label}"
            with open(path, "w") as f:
                f.write("")
