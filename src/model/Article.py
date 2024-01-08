class Article:

    def __init__(self, url, year, month, day) -> None:
        self.url = url
        self.year = year
        self.month = month
        self.day = day

    def to_json(self):
        return {"year" : self.year, "month" : self.month, "day" : self.day, "url" : self.url}