import unidecode
import re

class ArticleContent:

    count = 0

    def __init__(self, author, text_article) -> None:
        self.author = author
        self.text_article = self.clean(text_article)

    def clean(self, text_elem):

        text_elem = text_elem.strip()

        filter_to_space = ["_", ",", ";", ".", "-", ":", '"', "'", "«", "»"]
        
        for filter_ in filter_to_space:
            text_elem = text_elem.replace(filter_, " ")

        text_elem = re.sub("  ", " ", text_elem)
        text_elem = re.sub("   ", " ", text_elem)

        text_elem = unidecode.unidecode(text_elem)

        return text_elem

    def __repr__(self) -> str:
        return f"text_article : {self.text_article}\nauthor : {self.author}"
