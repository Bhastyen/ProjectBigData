import re

class Article:

    def __init__(self, title, year, abstract, author, linkPdf, dico_en, dico_fr, stop_word_en, stop_word_fr):
        # get data
        self.title = re.sub(r'[^\w\s]', "", str(title)).lower().split(" ")
        self.year = year
        self.abstract = re.sub(r'[^\w\s]', " ", str(abstract)).lower().split(" ")  # remove punctuations in abstract
        self.author = author.split(",")
        self.linkPdf = linkPdf
        self.dico_en = dico_en
        self.dico_fr = dico_fr
        self.stop_en = stop_word_en
        self.stop_fr = stop_word_fr
        self.english_text = False

        # detect if this article is in english or french language
        self.english_text = self.isEnglish()

        # remove stop word to process the text
        self.title = self.removeStopWord(self.title)
        self.abstract = self.removeStopWord(self.abstract)

        # correct wrong words in abstract
        self.preprocess()

    def preprocess(self):
        strange_word = []
        c1 = 0
        c2 = 0

        for w in self.abstract:
            c2 += 1
            if len(w) > 1 and w not in self.dico_en and w not in self.dico_fr:
                strange_word.append(w)
                c1 += 1

        #print(c1, c2)

        for w in strange_word:
            for i in range(len(w)-1, 0, -1):
                if w[:i] in self.dico_en or w[:i] in self.dico_fr:
                    #print("w1", w[:i], "w2", w[i:])
                    break

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
            if w not in self.stop_en and w not in self.stop_fr:
                tab.append(w)

        return tab

    def __repr__(self):
        english = "in_english"
        if not self.english_text:
            english = "in french"

        return "Article " + english + " with \n\tTitle " + str(self.title) + "\n\tYear " + str(self.year) + "\n\tAuthors " + str(self.author) + \
               "\n\tAbstract Length " + str(len(self.abstract)) + " Content " + str(self.abstract) + \
               "\n\tFrom " + str(self.linkPdf)