class Entry:
    def __init__(self, text, source_link, target_link, source_page="NONE", score=0.0):
        self.text = text
        self.source_link = source_link
        self.target_link = target_link
        self.score = round(score, 2)
        self.source_page = source_page

    def set_score(self, score):
        self.score = score

    def to_dict(self):
        return {"text": self.text,
                "source_link": self.source_link,
                "target_link": self.target_link,
                "score"      : self.score,
                "source_page": self.source_page}

    def __hash__(self):
        return hash(self.text)

    def __eq__(self, other):
        return self.text == other.text

    def __str__(self):
        return self.text
