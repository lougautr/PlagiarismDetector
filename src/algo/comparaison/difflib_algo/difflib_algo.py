import os
import difflib

#lecture et ouverture de tous les fichiers .txt dans le répertoire
class Difflib:
    #fonction de comparaison de difflib
    def compare(text1,text2):
        similarity = 0
        similarity = difflib.SequenceMatcher(None,text1,text2).ratio()
        
        if similarity > 0.5:
            return {"similarity" : round(similarity*100, 2), "result": True, "algo" : "difflib"}
        else:
            return {"similarity" : round(similarity*100, 2), "result": False, "algo" : "difflib"}
