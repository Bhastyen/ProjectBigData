from difflib import SequenceMatcher

import unidecode as unicode
import pandas as pd
import time, random

import unidecode as unidecode

from classes.Article import Article


path_to_dic_en = "dictionnary/words.txt"
path_to_dic_fr = "dictionnary/lexique-collecte.txt"
path_to_stop_fr = "dictionnary/stop-word-french.txt"
path_to_stop_en = "dictionnary/stop-word-en.txt"


def parse_article_from_csv(path_articles):
    data = pd.read_csv(path_articles, sep="\t")
    fichier_mot_dico = pd.read_csv(path_to_dic_fr, sep="\t", encoding="utf8")
    file_word_dico = open(path_to_dic_en, "r", encoding="utf8")
    file_stop_word_fr = open(path_to_stop_fr, "r", encoding="utf8")
    file_stop_word_en = open(path_to_stop_en, "r", encoding="utf8")

    articles = []
    stop_word_en = file_stop_word_en.readlines()
    stop_word_fr = file_stop_word_fr.readlines()
    word_dico = file_word_dico.readlines()
    mot_dico = fichier_mot_dico[["Flexion"]]
    mot_d = []

    # process the dictionnaries
    for i in range(len(word_dico)):
        word_dico[i] = word_dico[i].replace('\n', '').lower()

    for w in mot_dico["Flexion"]:
        mot_d.append(w.lower())

    # process lists of stop words
    for i in range(len(stop_word_en)):
        stop_word_en[i] = stop_word_en[i].replace('\n', '').lower()

    for i in range(len(stop_word_fr)):
        stop_word_fr[i] = stop_word_fr[i].replace('\n', '').lower()

    # garbage collector
    mot_dico = mot_d
    mot_d = []

    # create articles
    t = time.time()
    for (index, content) in data.iterrows():
        art = Article(str(content["title"]), int(content["year"]), str(content["abstract"]),
                      str(content["authors"]), content["pdfarticle"], word_dico, mot_dico,
                      stop_word_en, stop_word_fr)
        articles.append(art)
    print("Time to process", time.time() - t)

    file_word_dico.close()

    return articles

articles = parse_article_from_csv("data/export_articles_EGC_2004_2018.csv")
# print(articles[random.randrange(0, len(articles))])

def create_author_cluster(articles):
    authors = {}
    output = open("edge_list_authors.txt", "w", encoding="utf8")

    # create dictionnary of authors
    for art in articles:
        for auth1 in art.authors:
            for auth2 in art.authors:
                if auth1 != auth2:
                    if auth1 not in authors.keys():
                        authors[auth1] = {}
                    if auth2 not in authors[auth1].keys():
                        authors[auth1][auth2] = 0
                    authors[auth1][auth2] += 1

    # create matrix adjency in txt format for R programs
    for (auth1, colleagues) in authors.items():
        for (auth2, weight) in colleagues.items():
            if weight > 3:
                output.write(auth1 + " " + auth2 + " " + str(weight) + "\n")

    output.close()

#create_author_cluster(articles)


def create_topic_cluster(articles):
    results = {}
    titles = []
    output = open("edge_similarity_title_abstract.txt", "w", encoding="utf8")
    string = " "

    # create list of title
    for art in articles:
        titles.append(string.join(art.title))
        results[string.join(art.title)] = {}

    # create similarity table
    for art in articles:
        for title in titles:
            if title != string.join(art.title):
                results[title][string.join(art.title)] = SequenceMatcher(None, title, string.join(art.abstract)).ratio()

    # create matrix adjency in txt format for R programs
    for (title1, similarity) in results.items():
        for (title2, weight) in similarity.items():
            if weight > 0.45:
                output.write(unicode.unidecode(title1.split(" ")[0]) + " " + unicode.unidecode(title2.split(" ")[0]) + " " + str(weight) + "\n")
    output.close()


create_topic_cluster(articles)
