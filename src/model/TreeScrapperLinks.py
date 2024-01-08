from bs4 import BeautifulSoup
from calendar import monthrange
import json
from unidecode import unidecode

from src.model.RequestSave import requestAndSave
from src.model.Article import Article

class LiberationScrapper:

    def __init__(self, fistYear: int, lastYear: int, db, BASE_URL = "https://www.liberation.fr/archives/", scrap=False) -> None:
        self.years_list = []
        self.fistYear = fistYear
        self.lastYear = lastYear

        self.BASE_URL = BASE_URL

        if self.BASE_URL[-1] != "/":
            self.BASE_URL += "/"

        if self.fistYear > self.lastYear:
            raise Exception("first > last year")
        
        else:
            for i in range(self.fistYear, self.lastYear + 1):
                self.years_list.append(Year(str(i), self.BASE_URL, db, scrap))


    def to_json(self):
        return {"years_list" : [year.to_json() for year in self.years_list]}

    def save_json_to_file(self, path_file: str):
        json_ =  json.dumps(self.to_json())

        with open(path_file, "w", encoding="utf8") as f:
            f.write(json_)


class Year:

    def __init__(self, year_label: str, base_url: str, db, scrap=False,) -> None:
        self.year_label = year_label
        self.months_list = []

        self.YEAR_BASE_URL = base_url + self.year_label + "/"

        for i in range(1, 13):

            if i < 10:
                i = "0" + str(i)

            self.months_list.append(Month(str(i), monthrange(int(self.year_label), int(i))[1], self.YEAR_BASE_URL, scrap, db, self.year_label))

    def to_json(self):
        return {"year_label" : self.year_label,"months_list" : [month.to_json() for month in self.months_list]}


class Month:

    def __init__(self, month_label: str, nb_days: int, base_url: str, scrap, db, year_label) -> None:
        self.month_label = month_label
        self.days_list = []
        self.nb_days = nb_days

        self.MONTH_BASE_URL = base_url + self.month_label + "/"

        for i in range(1, self.nb_days+1):
            if i < 10:
                i = "0" + str(i)

            self.days_list.append(Day(str(i), self.MONTH_BASE_URL, scrap, db, year_label, month_label))

    def to_json(self):
        return {"month_label" : self.month_label,"days_list" : [day.to_json() for day in self.days_list]}



class Day:

    def __init__(self, day_label, base_url, scrap, db, year_label, month_label) -> None:
        self.day_label = day_label
        self.articleOfDay = []

        self.DAY_URL = base_url + day_label

        self.db = db
        self.year_label = year_label
        self.month_label = month_label


        if scrap:
            self.genArticles(self.db)


    def scrapLiberation(self, url):
        flag, r = requestAndSave(url)

        if not flag:
            return (False, "Request Error")

        soup = BeautifulSoup(r, 'html.parser')

        total = []
        for article in soup.findAll('a', attrs={'rel' : 'noreferrer'}, href=True) :

            link = article["href"]
            
            children = article.findChildren("h2" , recursive=False)

            if len(children) != 0:
                total.append(link)

        return (True, total)

    def genArticles(self, db):
        flag, duo = self.scrapLiberation(self.DAY_URL)

        if flag:

            [(self.articleOfDay.append(Article(link, self.year_label, self.month_label, self.day_label)), db.addArticle_researched_table(Article(link, self.year_label, self.month_label, self.day_label))) for link in duo]

         
    def to_json(self):
        return {"day_label" : self.day_label, "url" : self.DAY_URL, "articles" : [article.to_json() for article in self.articleOfDay]}


    
