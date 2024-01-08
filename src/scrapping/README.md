# Fonctionnement du scrapping

Nous avons scrappé les archives de Libération de 2018, 2019 et 2022.

Dans un premier lieu nous avons crée les liens de chacun des jours de chacune des années

www.liberation.fr/<annee>/<mois>/<jour>

Ensuite nous avons récupéré chaque lien d'article de ces pages, ces liens sont stockés dans le postgresql <researched_table>

Grâce a ces liens nous avons ensuite récupérée les informations voulu (auteur, contenu), et nous les avons stocké dans le postgres <articles_table>

## Execution des scripts

1- scrapLinkScript.py
2- scrapArticleScript.py