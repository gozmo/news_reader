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



def list_articles(source, label, all_entries):
    articles = io_utils.read_label(source, label)
    if source == Sources.BLOGS: 
        articles = sorted(articles, key=lambda x:x.publish_time, reverse=True)
    elif source == Sources.TWITTER:
        articles = sorted(articles, key=lambda x:x.publish_time, reverse=True)
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
        transformer_path = f"{BASE_PATH}/{source}/{TRANSFORMER_MODEL_NAME}"
        ffn_path = f"{BASE_PATH}/{source}/{FFN_MODEL_NAME}"
        transformer = Bert()
        transformer.load(transformer_path, ffn_path)

        dataset = ClassificationDataset(entities)
        classifications = transformer.classify(dataset)
        for score, entity in zip(classifications, entities):
            entity.set_score(score[0])


    for entity in tqdm(entities, desc="IO operations"):
        if not (io_utils.in_label(source, Labels.POSITIVE, entity) or \
                io_utils.in_label(source, Labels.NEGATIVE, entity) or \
                io_utils.in_label(source, Labels.UNLABELED, entity)):
            io_utils.append(source, Labels.LATEST, entity)
            io_utils.append(source, Labels.UNLABELED, entity)

    io_utils.remove_old_entries(source, Labels.LATEST, datetime.timedelta(hours=24))

def annotate(source, indices, label):
    articles = list_articles(source, Labels.LATEST, True)
    articles_to_annotate = [articles[idx] for idx in indices]

    for article in articles_to_annotate:
        if label == Labels.POSITIVE or label == Labels.NEGATIVE:
            io_utils.remove(source, Labels.LATEST, article)
            io_utils.remove(source, Labels.UNLABELED, article)

        io_utils.append(source, label, article)

def open(source, label, numbers):
    for number in numbers:
        articles = list_articles(source, label, True)
        article = articles[number]
        webbrowser.open(article.target_link)
    annotate(numbers, Labels.POSITIVE)

def train(source):
    dataset = TrainingDataset(source)

    bert = Bert()
    bert.train(dataset)
    bert.save(source)

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
