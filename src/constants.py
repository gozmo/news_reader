from pathlib import Path

BASE_PATH = f"{Path.home()}/Dropbox/news_reader/"

class Labels: 
    NEGATIVE = "negative"
    POSITIVE = "positive"
    LATEST = "latest"
    UNLABELED = "unlabeled"

class Sources:
    TWITTER = "twitter"
    NEWS = "news"
    BLOGS = "blogs"

class Twitter:
    CONSUMER_TOKEN = f"{BASE_PATH}/twitter/keys/consumer_token"
    CONSUMER_SECRET = f"{BASE_PATH}/twitter/keys/consumer_token_secret"
    ACCESS_TOKEN = f"{BASE_PATH}/twitter/keys/access_token"
    ACCESS_SECRET = f"{BASE_PATH}/twitter/keys/access_token_secret"

FFN_MODEL_NAME = "ffn_model.pth"
TRANSFORMER_MODEL_NAME = "transformer_model.pth"


DEVICE = "cpu"
