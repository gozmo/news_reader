class Entry:
    def __init__(self, text,
                       source_link,
                       publish_time,
                       score=0.0):
        self.text = text
        self.source_link = source_link
        self.score = round(score, 2)
        self.source_page = source_page
        
        if type(publish_time) == str:


        self.publish_time = publish_time

    def set_score(self, score):
        self.score = round(score, 2)

    def to_dict(self):
        return {"text": self.text,
                "link": self.link,
                "score"      : self.score,
                "source": self.source,
                "publish_time": self.publish_time.isoformat()}

    def __hash__(self):
        return hash(self.text)

    def __eq__(self, other):
        return self.text == other.text

    def __str__(self):
        return self.text
