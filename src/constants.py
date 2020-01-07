from pathlib import Path

class Labels: 
    NEGATIVE = "negative"
    POSITIVE = " positive"
    LATEST = "latest"
    UNLABELED = "unlabeled"


class Paths:
    HOME = str(Path.home())
    NEGATIVE= f"{HOME}/Dropbox/hackernews/negative.jsonl"
    POSITIVE= f"{HOME}/Dropbox/hackernews/positive.jsonl"
    UNLABELED= f"{HOME}/Dropbox/hackernews/unlabeled.jsonl"
    LATEST= f"{HOME}/Dropbox/hackernews/latest.jsonl"


    BERT_MODEL = f"{HOME}/Dropbox/hackernews/bert.pt"
    FFN_MODEL = f"{HOME}/Dropbox/hackernews/ffn_model.pt"

DEVICE = "cpu"
