from src.model.ArticleContent import ArticleContent
from src.model.RequestSave import requestAndSave

from bs4 import BeautifulSoup


class ArticleScrapper:

    def __init__(self, article) -> None:
        self.article = article
        self.BASE_URL = "https://www.liberation.fr"

        self.getCompleteUrl()

    def getCompleteUrl(self):
        self.full_url = self.BASE_URL + self.article.url
    
    def scrap(self):
        flag, r = requestAndSave(self.full_url)

        if not flag:
            return genNegativeArticleContent()

        soup = BeautifulSoup(r, 'html.parser')
        
        # Get if this article is premium
        premium = soup.find_all("div", class_ = "TypologyArticle__BlockPremium-sc-1vro4tp-2")

        if premium != []:
            return genNegativeArticleContent()

        # Get author
        author = soup.find_all("meta", property="article:author")
        if author == []:
            return genNegativeArticleContent()
        
        else:
            author = author[0]["content"]

        # Get paragraphe
        all_text = " ".join([elem.text for elem in soup.find_all("p", class_ = "article_link")])

        article = ArticleContent(author, all_text)
        
        return article

def genNegativeArticleContent():
    return ArticleContent("ERROR", "ERROR")