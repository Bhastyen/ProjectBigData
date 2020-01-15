import pandas as pd
import time
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

print(articles[0])
