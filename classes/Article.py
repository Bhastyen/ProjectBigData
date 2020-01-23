import re

import requests
from translate import Translator

class Article:

    def __init__(self, title, year, abstract, author, linkPdf, dico_en, dico_fr, stop_word_en, stop_word_fr):
        # get data
        self.title = re.sub(r'[^\w\s]', "", str(title)).lower().split(" ")
        self.year = year
        self.abstract = re.sub(r'[^\w\s]', " ", str(abstract)).lower().split(" ")  # remove punctuations in abstract
        self.authors = author.split(",")
        self.linkPdf = linkPdf
        self.dico_en = dico_en
        self.dico_fr = dico_fr
        self.stop_en = stop_word_en
        self.stop_fr = stop_word_fr
        self.english_text = False

        # process authors to remove spaces
        for i in range(len(self.authors)):
            if self.authors[i][0] == " ":
                self.authors[i] = self.authors[i][1:]
            self.authors[i] = self.authors[i].replace(" ", "_")

        # detect if this article is in english or french language
        self.english_text = self.isEnglish()

        # remove stop word to process the text
        self.title = self.removeStopWord(self.title)
        self.abstract = self.removeStopWord(self.abstract)

        # correct wrong words in abstract
        if self.english_text:
            self.preprocess(self.stop_en, self.dico_en)
        else:
            self.preprocess(self.stop_fr, self.dico_fr)
            # traduction en anglais
            title_en = []
            for s in self.title:
                title_en.append(Translator('en', 'fr', 'mymemory').translate(s))
            self.title = title_en
            abstract_en = []
            for s in self.abstract:
                abstract_en.append(Translator('en', 'fr', 'mymemory').translate(s))
            self.abstract = abstract_en

            # string = " "
            # url = 'http://translate.google.com/translate_a/t'
            # params = {
            #         "text": string.join(self.title),
            #         "sl": "fr",
            #         "tl": "en",
            #         "client": "p"
            # }
            # self.title = requests.get(url, params=params).content
            # params = {
            #         "text": string.join(self.abstract),
            #         "sl": "fr",
            #         "tl": "en",
            #         "client": "p"
            # }
            # self.abstract = requests.get(url, params=params).content




    def preprocess(self, stop_word, dico):
        strange_word = []
        insert = []
        c1, c2 = 0, 0
        shift = 0

        # search word which are not recognize
        for w in self.abstract:
            c2 += 1
            if len(w) > 1 and w not in dico:
                strange_word.append((w, c2))
                c1 += 1
        #print(c1, c2)

        #print("Avant", self.abstract)

        # search two new words from a detected strange word
        for (w, index) in strange_word:
            for i in range(len(w)-1, 0, -1):
                if w[:i] in dico:
                    if w[:i] not in stop_word and w[i:] not in stop_word:
                        insert.append(w[:i])
                        insert.append(w[i:])
                        self.abstract = self.abstract[:index + shift - 1] + insert + self.abstract[index + shift:]
                        shift += 1
                    elif w[:i] not in stop_word and w[i:] in stop_word:
                        insert.append(w[:i])
                        self.abstract = self.abstract[:index + shift - 1] + insert + self.abstract[index + shift:]
                    elif w[:i] in stop_word and w[i:] not in stop_word:
                        insert.append(w[i:])
                        self.abstract = self.abstract[:index + shift - 1] + insert + self.abstract[index + shift:]
                    elif w[:i] in stop_word and w[i:] in stop_word:
                        self.abstract = self.abstract[:index + shift - 1] + self.abstract[index + shift:]
                        shift -= 1
                    insert = []
                    break

        #print("Apres", self.abstract)

    def isEnglish(self):
        l = len(self.abstract)
        english_word = 0
        french_word = 0

        for w in self.abstract:
            if w in self.stop_en:
                english_word += 1
            if w in self.stop_fr:
                french_word += 1
        #print("ratio french word", french_word/l, "ratio english word", english_word/l)

        return english_word/l > french_word/l

    def removeStopWord(self, data):
        tab = []

        for w in data:
            if self.english_text:
                if w not in self.stop_en:
                    tab.append(w)
            elif w not in self.stop_fr:
                tab.append(w)
        return tab

    def __repr__(self):
        english = "in_english"
        if not self.english_text:
            english = "in french"

        return "Article " + english + " with \n\tTitle " + str(self.title) + "\n\tYear " + str(self.year) + "\n\tAuthors " + str(self.authors) + \
               "\n\tAbstract Length " + str(len(self.abstract)) + " Content " + str(self.abstract) + \
               "\n\tFrom " + str(self.linkPdf)