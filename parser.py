from difflib import SequenceMatcher

import unidecode as unicode
import pandas as pd
import time, random
import os, re
import unidecode as unidecode
import wget, pdfx
from classes.Article import Article


# path to resources
path_to_dic_en = "dictionnary/words.txt"
path_to_dic_fr = "dictionnary/lexique-collecte.txt"
path_to_stop_fr = "dictionnary/stop-word-french.txt"
path_to_stop_en = "dictionnary/stop-word-en.txt"

# hyper-parameters
ref_author = True
min_number_of_common_works = 15
number_of_top = 10

def find_ref(refs):
    result = []
    groups = re.search(r'[A-Z][a-z\-]*\s*,\s*[A-Z]|(,\s*|(et|and)\s*)[A-Z]\s*[A-Z]\s*[A-Za-zç\-\']*', refs)

    if groups:
        value = groups.group()
        # process the beginning of name
        if value.startswith(",et"):
            value = value[3:]
        elif value.startswith(", et"):
            value = value[4:]
        elif value.startswith(" et"):
            value = value[3:]
        elif value.startswith("et"):
            value = value[2:]
        elif value.startswith(",and"):
            value = value[4:]
        elif value.startswith(", and"):
            value = value[5:]
        elif value.startswith(" and"):
            value = value[4:]
        elif value.startswith("and"):
            value = value[3:]
        elif value.startswith(","):
            value = value[1:]

        if value.startswith(" "):
            value = value[1:]
        elif value.startswith("  "):
            value = value[2:]

        # change the form to get always the same format of name
        if re.match(r'[A-Za-z\-]*\s*,\s*[A-Z]', value):
            value = value[value.find(",") + 1:] + " " + value[:value.find(",")]

        # process the spaces at the beginning of name
        if value.startswith(" "):
            value = value[1:]
        elif value.startswith("  "):
            value = value[2:]

        # process the spaces at the end of name
        if value.endswith(" "):
            value = value[:-1]
        elif value.endswith("  "):
            value = value[:-2]

        # last verification to remove common words
        if re.match(r'[A-Z](\s|-)', value):
            result.append(value)

        return result + find_ref(refs[groups.span()[1]:])

    return result


def get_references(url, id, length_of_data):
    refs = ""
    marker = -1
    content_pdf = []
    reference_find = False

    # clean the pdf directory if need
    download_again = len(os.listdir("data/pdf")) < length_of_data
    if download_again:
        for f in os.listdir("data/pdf"):
            os.remove("data/pdf/" + f)

    # download if need
    if download_again:
        wget.download(url, "data/pdf/" + id + ".pdf")

    # get references of pdf article
    try:
        pdf = pdfx.PDFx("data/pdf/" + id + ".pdf")
        text = pdf.get_text()
        pages = text.split("\n\n")

        for p in range(len(pages) - 1, 0, -1):   # we search on each page p from the end ...
            for s in pages[p].split("."):   # ... on each sentence s ...
                if "References" in s or "Références" in s:  # ... the page with references part
                    marker = p
                    break
            if marker != -1:
                break

        if marker != -1:
            for p in range(marker, len(pages)):   # we process only the pages with references
                for s in pages[p].split("."):
                    if reference_find or "References" in s or "Références" in s:  # ... the page with references part
                        refs += s.replace("\n", "") + " "  # we keep all characters after the references have benn found
                        reference_find = True

        if refs != "":  # if we have references in this article
            for r in re.split(r'\([1-2][0-9][0-9][0-9]\)', refs):
                content_pdf.append(find_ref(unidecode.unidecode(r)))   # we search the name of authors

    except: print("Failed", id)

    return content_pdf


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
    c = 0
    nb_art = 0
    t = time.time()
    for (index, content) in data.iterrows():
        if nb_art > -1:
            url = str(content["pdfarticle"])
            id = url[url.find("?") + 3:]
            contentPdf = []
            if ref_author:
                contentPdf = get_references(url, id, len(data.index))
                if not contentPdf:
                    c += 1
            art = Article(id, str(content["title"]), int(content["year"]), str(content["abstract"]),
                          unidecode.unidecode(str(content["authors"])), contentPdf, word_dico, mot_dico,
                          stop_word_en, stop_word_fr)
            articles.append(art)
            print(articles[-1].id, len(articles[-1].references), articles[-1].references)
            print("--------------------------------------------------------------------")
        nb_art += 1

    # we print the number of articles unprocessed
    print("Article unprocessed", c, "Article Processed", (len(articles) - c))
    # print th total time to process all articles
    print("Time to process", time.time() - t)

    file_word_dico.close()

    return articles

def create_author_cluster(articles):
    authors = {}
    dejavu = []
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
            if weight >= min_number_of_common_works and (auth1, auth2) not in dejavu and (auth2, auth1) not in dejavu:
                output.write(auth1 + " " + auth2 + " " + str(weight) + "\n")
                dejavu.append((auth1, auth2))

    output.close()

def create_author_references_cluster(articles):
    authors = {}
    dejavu = []
    output = open("edge_list_authors_references.txt", "w", encoding="utf8")

    # create dictionnary of authors
    for art in articles:
        for auths in art.references:
            for auth1 in auths:
                for auth2 in auths:
                    if auth1 != auth2:
                        if auth1 not in authors.keys():
                            authors[auth1] = {}
                        if auth2 not in authors[auth1].keys():
                            authors[auth1][auth2] = 0
                        authors[auth1][auth2] += 1

    # create matrix adjency in txt format for R programs
    for (auth1, colleagues) in authors.items():
        for (auth2, weight) in colleagues.items():
            if weight >= min_number_of_common_works and (auth1, auth2) not in dejavu and (auth2, auth1) not in dejavu:
                output.write(auth1 + " " + auth2 + " " + str(weight) + "\n")
                dejavu.append((auth1, auth2))

    output.close()


def create_author_references_distribution(articles):
    authors = {}
    output = open("distribution_author_quoted.csv", "w", encoding="utf8")

    # create dictionnary of authors with the number of references
    for art in articles:
        for auths in art.references:
            for auth in auths:
                if auth not in authors.keys():
                    authors[auth] = 0
                authors[auth] += 1

    # sort the items of dictionnary
    most_quotation = sorted(authors.items(), reverse=True, key=lambda tup: tup[1])
    print(most_quotation[:number_of_top])

    # create csv with in first column, the author, and in second column, the "frequency"
    output.write("author,n_references\n")
    for (auth, number_references) in most_quotation[:number_of_top]:
        output.write(auth + "," + str(number_references) + "\n")

    output.close()


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


# get articles and their content
articles = parse_article_from_csv("data/export_articles_EGC_2004_2018.csv")

# write a graph to see the authors having often work together
create_author_cluster(articles)
# create a distribution to see what author have been most quoted in all articles
create_author_references_distribution(articles)
# create a graph to see the authors who work between them
create_author_references_cluster(articles)
# create data to calculate cluster of topics
create_topic_cluster(articles)

#print(articles[random.randrange(0, len(articles))])
