import dateutil.parser

class Entry:
    def __init__(self, text,
                       link,
                       publish_time: str,
                       source,
                       score=0.0):
        self.text = text
        self.link = link
        self.set_score(score)
        self.source = source
        self.publish_time = dateutil.parser.parse(publish_time)

    def set_score(self, score):
        self.score = score

    def to_dict(self):
        return {"text": self.text,
                "source_link": self.source_link,
                "score"      : self.score,
                "publish_time": self.publish_time.isoformat(),
                "source_page": self.source_page}

    def __hash__(self):
        return hash(self.text)

    def __eq__(self, other):
        return self.text == other.text

    def __str__(self):
        return self.text
