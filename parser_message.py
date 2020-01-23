
import os
import zipfile
import re

import pandas as pd

from Message import Message
import fnmatch
import unidecode

zfile = os.listdir("data/messages")
#with zipfile.ZipFile('data/liste2016_2018.zip', 'r') as zipObj:
   # Extract all the contents of zip file in current directory
 #  zipObj.extractall("data/messages")
#ata = zfile.read(filename)
#file = open(filename, 'w+b')
i = 0

path_to_dic_en = "dictionnary/words.txt"
path_to_dic_fr = "dictionnary/lexique-collecte.txt"
path_to_stop_fr = "dictionnary/stop-word-french.txt"
path_to_stop_en = "dictionnary/stop-word-en.txt"

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

def searchMessage(nameFile,year):
    #filetest = open("data/messages/polytech_liste-egc_2016-07/1", "r", encoding="utf8")
    #filewrite = open("data/test.txt", 'w', encoding="utf8")

    fileMessage = open(nameFile, "r", encoding="latin1")

    s = ""
    m=" "
    subjectFind = False
    beginContent = False
    endContent = False
    content = ""
    author =""
    sujet =""
    # Detection du auteur/ sujet / contenu message /

    for l in fileMessage.readlines():
        if re.match(r'Return-Path: ', l):  # retourne l'auteur du mail
            l= l[:-1]
            author = re.sub(r"[<>]", "", l.split(" ")[1])
        elif re.match(r'Subject: ', l):  # retourne le sujet du mail
            sujet = re.sub(r"[<>]", "", m.join(l.split(" ")[1:-1]))
            subjectFind = True
        elif subjectFind and not beginContent:  # retourne le contenu du mail
            #content = ""
            if not re.match(r'[A-Za-z\-_0-9]+:|\s+|--+', l):
                content += l
                beginContent = True
        elif beginContent and not endContent:
            if re.match(r'--+[A-Za-z]|-+', l):
                endContent = True
            else:
                content += l
    
    print("Content", content)
    print("Content End ----------------------------")
    
    # correction in file with hex code
    sujet = preprocessEncoding(sujet)
    content = preprocessEncoding(content)
    print("Content APRES processing",content)
    fileMessage.close()
    return Message(sujet,year,author,content,word_dico,mot_d,stop_word_en,stop_word_fr)


def getNameFile(dirName):
    listFile = []

    if not os.path.isdir(dirName):
        return [dirName]

    list = os.listdir(dirName)
    for d in list:
        if os.path.isfile(d):
            listFile.append(d)
        else:
            listFile += getNameFile(dirName + "/" + d)
    print("taille files" + str(len(listFile)))
    print(listFile)
    return listFile


def creationAuteurNbMessage(year,messages) :
    auteurAnnee = {}
    for m in messages:
        # Creation du graphe auteurs/ annee nombre d'envoie
        if m.authors not in auteurAnnee:
            auteurAnnee[m.authors] = 0
        auteurAnnee[m.authors] += 1
    auteurAnnee = sorted(auteurAnnee.items(), key=lambda t: t[1], reverse=True)

    print(len(auteurAnnee))

    print(auteurAnnee)
    # Creation annee - sujet des messages
    graph = open("data/graph_messages_auteurs_" + year + ".txt", 'w', encoding="utf8")
    for key, value in auteurAnnee[:10]:
        name = unidecode.unidecode(key)
        weight = str(value)
        stra = name + " " + year + " " + weight + "\n"
        print(stra)
        graph.write(stra)

    print(len(auteurAnnee))
    print(len(messages))
    graph.close()

def creationDocumentFromMessage(messages):
    i=0
    chaine = " "
    for m in messages :
        year = m.year
        doc = open("data/documents_messages/"+year+"/"+str(i),"w")
        i+=1
        doc.writelines(chaine.join(m.subject)+" ")
        doc.writelines(chaine.join(m.message))

def creationMessages(year):

    messages = [] #liste des messages disponible
    for filename in getNameFile("data/messages"):

        # if os.path.isdir(filename):#Si c'est un dossier (marche pas)

        if fnmatch.fnmatch(filename, "*"+year+"*") and not fnmatch.fnmatch(filename, "*/"):
            print(filename)
            messages.append(searchMessage(filename,year))
    return messages


def preprocessEncoding(s):
    s = s.replace("\n", "")
    s = re.sub(r'(=+C3)?=+A9', "é", s)
    s = re.sub(r'(=+C3)?=+A8', "è", s)
    s = re.sub(r'=+E2=+80=+99', "'", s)
    s = re.sub(r'(=+C3)?=+A7', "ç", s)
    s = re.sub(r'(=+C3)?=+A0', "à", s)
    s = re.sub(r'(=+C3)?=+AA', "ê", s)
    s = re.sub(r'(=+C3)?=+B9', "ù", s)
    s = re.sub(r'(=+C3)?=+B4', "ô", s)
    s = re.sub(r'(=+C3)?=+AE', "î", s)
    s = re.sub(r'=20', " ", s)
    s = s.replace("=", "")
    return  s

messages = creationMessages("2016")
#creationAuteurNbMessage("2017",messages)
creationDocumentFromMessage(messages)
'''
   if fnmatch.fnmatch(filename, "*2016*") and not fnmatch.fnmatch(filename, "*/"):
            print(filename)
            try:
                messages.append(searchMessage(filename,"2016"))
                file = open("data/messages/" + filename, "r", encoding="utf8")
                #for line in file.readlines():
                   # print(line)

            except:
                pass
                # file = open("data/messages/" + filename, "r", encoding="latin1")
                # for line in file.readlines():
                #    print(line)
'''