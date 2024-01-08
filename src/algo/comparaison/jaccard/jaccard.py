import os


class Jaccard:
    #fonction de jaccard
    def jaccard(a,b):
        a = set(a.split())
        b = set(b.split())
        return len(a.intersection(b)) / len(a.union(b))

    #calcul de la similarité de jaccard
    def compare(text1,text2):
        jaccard_similarity = 0
        jaccard_similarity = Jaccard.jaccard(text1,text2)

        if jaccard_similarity > 0.5:
            return {"similarity" : round(jaccard_similarity, 2) * 100, "algo" : "jaccard", "result" : True}
        else:
            return {"similarity" : round(jaccard_similarity, 2) * 100, "algo" : "jaccard", "result": False}