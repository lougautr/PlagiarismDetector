"""
Virer les premium :
div class="TypologyArticle__BlockPremium-sc-1vro4tp-2"

Auteur :
span a | dernier element
recuperer le href et check si il y le mot auteur dedans

Texte :
article class="article-body-wrapper"
"""

import sys
import path
 
db = path.Path("../corpus/DBInterface.py").abspath() 
builder = path.Path("../model/ArticleBuilder.py").abspath() 
scrapper = path.Path("../model/ArticleScrapper.py").abspath() 

sys.path.append(db.parent.parent)
sys.path.append(builder.parent.parent)
sys.path.append(scrapper.parent.parent)

from src.corpus.DBInterface import ScrapDatabase
from src.model.ArticleBuilder import ArticleBuilder
from src.model.ArticleScrapper import ArticleScrapper

"""
Depuis les liens récupéré dans la 
base de donnée et d'une année spécifiée, 
ce script scrap les articles correspondant 
et les charge dans la base de donnée
"""

"""
1 - Charger les données
2 - Scrap chaque article
3 - Stocker en base de données
"""

if __name__ == "__main__":

    year = int(sys.argv[1])
    availableYear = [2018, 2019, 2022, 2021]

    if year in [2018, 2019, 2022, 2021]:
        db = ScrapDatabase()

        articles = ArticleBuilder.multiBuild(db.readYear_researched_table(str(year)))

        for a in articles:
            content = ArticleScrapper(a).scrap()

            db.addInDb(content)

    else:
        print(f"Mauvaise date, dispo : {availableYear}")
