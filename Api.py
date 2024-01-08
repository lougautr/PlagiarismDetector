import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.algo.classification.bayes.Bayes import *
from src.algo.comparaison.difflib_algo.difflib_algo import *
from src.algo.comparaison.jaccard.jaccard import *
from src.algo.comparaison.vecteursCosinus.vecteurs_cosinus import *
#from src.algo.comparaison.vecteursCosinus.techniques_vecteurs_cosinus import *

from src.corpus.DBInterface import ScrapDatabase
from config import *


db = ScrapDatabase()
test, train = db.getTestTrainCorpus()
templates = Jinja2Templates(directory="./view")
app = FastAPI()



#L'Api génère le fichier index.html à la racine
@app.get("/")
def htmlFunction(request: Request):
    return templates.TemplateResponse("index.html", {"request" : request, "LISTE_ALGO_COMPARAISON" : LISTE_ALGO_COMPARAISON})


@app.post("/verif")
async def receive_data(request: Request):
    data = await request.json()
    
    #Si le dictionnaire data est de longueur 3, c'est forcément des données venant de la partie comparaison
    if len(data) == 3:
        print(data)

        if data["algo"] == "Jaccard":
            result = Jaccard.compare(data["file1"], data["file2"])
            
        elif data["algo"] == "Vecteur Cosinus":
            result = VecteurCos.compare(data["file1"], data["file2"])

        elif data["algo"] == "Difflib":
            result = Difflib.compare(data["file1"], data["file2"])
        
        else:
            result = {"algo" : "error", "result" : "error", "similarity" : "error"}

        with open("result.json", "w") as f:
            f.write(json.dumps(result))

        return {"status" : "ok"}
        
    #Si la taille est 2, c'est donc la partie classification
    elif len(data) == 2:

        if data["verif"] == "simi":
            print("Début Similarité Bayes")
            bayes = Bayes(db.readAll_articles_table(), data["file"])
            author = bayes.chooseClass(option=1)
            words = bayes.mostUsedWords(author, option=1)
            print(words)
            print("Fin Similarité Bayes")

            result = {"algo" : "Bayes", "author" : author, "words" : words}

        elif data["verif"] == "auteur":
            print("Début Auteur Bayes")
            bayes = Bayes(db.readAll_articles_table(), data["file"])
            author = bayes.chooseClass(option=1)
            print("Fin Auteur Bayes")

            result = {"algo" : "Bayes", "author" : author, "words" : []}

        else:
            result = {"algo" : "error", "author" : "error", "words" : []}

        with open("result.json", "w") as f:
            f.write(json.dumps(result))

    
@app.get("/comparaison")
async def comparaison(request: Request):

    while True:
        try:
            with open("result.json", "r") as f:
                result = json.load(f)
                print(result)
                break
        except Exception as e:
            pass
    
    if result["algo"] == "Bayes":
        return bayesResponse(request, result)
    
    return htmlResponse(request, result)

def bayesResponse(request: Request, result):
    context = {"request" : request} | result
    return templates.TemplateResponse("resultPageClassification.html", context)


def htmlResponse(request: Request, result):
    context = {"request" : request} | result
    return templates.TemplateResponse("resultPageComparaison.html", context)

import uvicorn

if __name__ == "__main__":
   uvicorn.run("Api:app", port=8000, log_level="info", host="localhost", reload=True)

