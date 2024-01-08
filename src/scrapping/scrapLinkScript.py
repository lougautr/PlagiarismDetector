import path
import sys
 
db = path.Path("../corpus/DBInterface.py").abspath() 
tree = path.Path("../model/TreeScrapperLinks.py").abspath() 

sys.path.append(db.parent.parent)
sys.path.append(tree.parent.parent)

from src.corpus.DBInterface import ScrapDatabase
from src.model.TreeScrapperLinks import LiberationScrapper

if __name__ == "__main__":


    firstYear = int(sys.argv[1])
    lastYear = int(sys.argv[2])

    db = ScrapDatabase()

    scrap = LiberationScrapper(firstYear, lastYear, db, scrap=False)
