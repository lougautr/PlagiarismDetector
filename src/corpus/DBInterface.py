import psycopg2
import json, random
from src.model.ArticleContent import ArticleContent

# Copy ---

class DBInterface:
    def __init__(self, pathInfoFile="./src/corpus/info.json"):
        f = open(pathInfoFile)
        data = json.load(f)
        f.close()

        self.conn = psycopg2.connect(
            host = data["host"],
            database = data["database_name"],
            user = data["user"],
            password = data["password"],
            port = data["port"]
        )

        self.cur = self.conn.cursor()

    def closeConnection(self):
        self.conn.close()


class ScrapDatabase(DBInterface):
    
    def __init__(self):
        super().__init__()

    def addArticle_researched_table(self, article):
        self.cur.execute("INSERT INTO researched_table (year, month, day, url) VALUES (%s, %s, %s, %s);", (article.year, article.month, article.day, article.url))
        self.conn.commit()

        return True

    def readAll_researched_table(self, limit:int=None):
        if limit == None:
            self.cur.execute("SELECT * FROM researched_table;")
            return self.cur.fetchall()

        else:
            self.cur.execute("SELECT * FROM researched_table LIMIT %s;", (limit, ))
            return self.cur.fetchall()

    def readYear_researched_table(self, year):
        self.cur.execute("SELECT * FROM researched_table WHERE year=%s;", (year, ))

        return self.cur.fetchall()

    def getArticleFromId_researched_table(self, id):
        self.cur.execute("SELECT * FROM researched_table WHERE id=%s;", (id,))
        
        return self.cur.fetchone()

    def addArticle_articles_table(self, articleContent:ArticleContent):

        def checkIfNegative(articleContent):
            if articleContent.author == "ERROR" and articleContent.text_article == "ERROR":
                return True

            return False

        if not checkIfNegative(articleContent):

            self.cur.execute("INSERT INTO articles_table (author, text_article) VALUES (%s, %s);", (articleContent.author, articleContent.text_article))
            self.conn.commit()
            return True

        return False
    
    def addInDb(self, article: ArticleContent):
        print(ArticleContent.count)
        ArticleContent.count += 1
        self.addArticle_articles_table(article)


    # ------------------ #

    def getArticleFromId_articles_table(self, id):
        self.cur.execute("SELECT * FROM articles_table WHERE id=%s;", (id,))
        
        data = self.cur.fetchall()[0]
        return ArticleContent(data[1], data[2])

    def readAll_articles_table(self, limit:int=None):
        if limit == None:
            self.cur.execute("SELECT * FROM articles_table;")

            datas = self.cur.fetchall()
            return [ArticleContent(data[1], data[2]) for data in datas]

        else:
            self.cur.execute("SELECT * FROM articles_table LIMIT %s;", (limit, ))
            
            datas = self.cur.fetchall()
            return [ArticleContent(data[1], data[2]) for data in datas]

    def getArticleFromAuthor_articles_table(self, author):
        self.cur.execute("SELECT * FROM articles_table WHERE author=%s;", (author,))

        datas = self.cur.fetchall()
        return [ArticleContent(data[1], data[2]) for data in datas]

    def getTestTrainCorpus(self):

        allData = self.readAll_articles_table()

        random.shuffle(allData)

        total = len(allData)

        id_test = int(total * 20 / 100)

        return (allData[:id_test], allData[id_test:])
