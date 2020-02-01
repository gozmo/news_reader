from pathlib import Path

class Labels: 
    NEGATIVE = "negative"
    POSITIVE = "positive"
    LATEST = "latest"
    UNLABELED = "unlabeled"

class Sources:
    TWITTER = "twitter"
    NEWS = "news"
    BLOGS = "blogs"

FFN_MODEL_NAME = "ffn_model.pth"
TRANSFORMER_MODEL_NAME = "transformer_model.pth"

BASE_PATH = f"{Path.home()}/Dropbox/news_reader/"

DEVICE = "cpu"
