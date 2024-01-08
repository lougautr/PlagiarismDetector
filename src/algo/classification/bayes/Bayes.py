import math
import sys

class Bayes:

    def __init__(self, dataTrain, dataTest):
        self.dataTrain = dataTrain
        self.dataTest = dataTest

    #Fonction qui compte le nombre de fois qu'un auteur apparait dans le corpus
    def countClass(self, data):
        count = {}
        for row in data:
            if row.author not in count:
                count[row.author] = 0
            count[row.author] += 1
        return count

    #Fonction qui compte le nombre de fois qu'un mot apparait dans le texte d'un auteur
    def countOccurenceWordsClasse(self, data):
        count = {}
        for row in data:
            if row.author not in count:
                count[row.author] = {}
            for word in row.text_article.split():
                    if word not in count[row.author]:
                        count[row.author][word] = 0
                    count[row.author][word] += 1
        return count

    #Fonction qui compte le nombre de mots dans tout les textes d'un auteur
    def countWordsClasse(self, data):
        count = {}
        for row in data:
            if row.author not in count:
                count[row.author] = 0
            for word in row.text_article.split():
                    count[row.author] += 1
        return count

    #Fonction qui compte le nombre de mots differents dans le corpus
    def countWordsDifferent(self, data):
        count = {}
        for row in data:
            for word in row.text_article.split():
                    if word not in count:
                        count[word] = 0
        return len(count)

    #Fonction qui calcule l'auteur qui a le plus de chance d'avoir écrit le texte
    #Les variables option et texte nous servent pour calculer l'efficacité du classificateur ou juste l'utiliser
    def chooseClass(self, texte="", option=0):
        if texte == "":
            texte = self.dataTest
        count = self.countClass(self.dataTrain)
        countWords = self.countWordsClasse(self.dataTrain)
        countWordsDifferents = self.countWordsDifferent(self.dataTrain)
        countOccurenceWords = self.countOccurenceWordsClasse(self.dataTrain)
        prob = {}
        #Pour chaque auteur, on calcule la probabilité qu'il ait écrit le texte
        for classe in count:
            prob[classe] = count[classe]/len(self.dataTrain)
            for word in texte.split():
                    if word in countOccurenceWords[classe]:
                        #On calcule le nombre de fois ou le mot apparait dans la classe + 1 pour éviter les 0 
                        # diviser par le nombre de mots dans la classe + le nombre de mots differents
                        #On utilise des logs pour éviter les problèmes de Underflow
                        prob[classe] += math.log((countOccurenceWords[classe][word] + 1) / (countWords[classe] + countWordsDifferents))
                    else:
                        prob[classe] += math.log(1/(countWords[classe] + countWordsDifferents))
        if option == 1:
            return max(prob, key=prob.get)
        return print("Le fichier a le plus de probabilité d'être de la classe: " + max(prob, key=prob.get))
    
    #Fonction qui calcule les mots les plus utilisés par un auteur dans le texte qu'on lui donne
    def mostUsedWords(self, author, option=0):
        wordsCommon = {}
        wordsUsed = self.countOccurenceWordsClasse(self.dataTrain)
        wordsUsedByAuthor = wordsUsed[author]
        for words in self.dataTest.split():
            if words in wordsUsedByAuthor:
                if words not in wordsCommon:
                    wordsCommon[words] = 1
                else:
                    wordsCommon[words] += 1
        wordsCommon = {k: v for k, v in wordsCommon.items() if v > 1}
        wordsCommon = sorted(wordsCommon.items(), key=lambda x: x[1], reverse=True)
        if option == 0:
            print("les mots les plus utilisés par l'auteur sont: " + wordsCommon)

        return wordsCommon
    
    def readAllData(self):
        data = []
        cpt = 1
        nbrArg = len(sys.argv)
        while cpt < nbrArg:
            with open(sys.argv[cpt], "r") as f:
                dataText = []
                for line in f.readlines():
                    dataTemp = line.split()
                    dataText += dataTemp
                data.append(dataText)
            cpt += 1
        return data
    
    #Ces fonctions servent à calculer l'efficacité du classificateur
    
    #On filtre les données de test pour ne garder que les auteurs qui sont dans le corpus d'entrainement
    def filtre(self, dict):
        data = []
        for article in self.dataTrain:
            if article.author in dict.keys():
                data.append(article)
        self.dataTrain = data
    
    #On crée une matrice afin de pouvoir stocker les résulats de l'efficacité du classificateur
    def matriceEfficacite(self):
        dict = {}
        cpt = 0
        for article in self.dataTest:
            for row in self.dataTest:
                if row.author not in dict:
                    dict[row.author] = cpt
                    cpt += 1
        matrice = [[0 for i in range(len(dict))] for j in range(len(dict))]
        return dict, matrice
    
    #On remplit la matrice avec les résultats de l'efficacité du classificateur
    #Les lignes correspondents à l'auteur réel et les colonnes à l'auteur prédit
    def remplirMatrice(self):
        dict, matrice = self.matriceEfficacite()
        self.filtre(dict)
        for article in self.dataTest:
            matrice[dict[article.author]][dict[self.chooseClass(article.text_article, 1)]] += 1
        
        for i in range(len(matrice)):
            phrase = ""
            for j in range(len(matrice[i])):
                phrase += matrice[i][j].__str__()+ " "
            #print(phrase)
        return matrice
    
    #On calcule l'efficacité du classificateur
    def recall(self, data):
        count = 0
        for i in range(len(data)):
            countRow = 0
            for j in range(len(data[i])):
                countRow += data[i][j]
            if countRow != 0:
                count += data[i][i]/countRow
        return count/len(data)

    #On calcule la précision du classificateur
    def precision(self, data):
        count = 0
        for i in range(len(data)):
            countColumn = 0
            for j in range(len(data[i])):
                countColumn += data[j][i]
            if countColumn != 0:
                count += data[i][i]/countColumn
        return count/len(data)
        