from src.model.Article import Article

class ArticleBuilder:

    def build(data):
        return Article(data[4], data[1], data[2], data[3])

    def multiBuild(datas):
        return [Article(data[4], data[1], data[2], data[3]) for data in datas]
