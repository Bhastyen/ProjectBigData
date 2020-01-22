import re
class Message:

    def __init__(self, subject, year,author, message ,dico_en, dico_fr, stop_word_en, stop_word_fr):
        # get data
        self.subject = re.sub(r'[^\w\s]', "", str(subject)).lower().split(" ")
        self.year = year
        self.message = re.sub(r'[^\w\s]', " ", str(message)).lower().split(" ")  # remove punctuations in abstract
        self.authors = author
        self.dico_en = dico_en
        self.dico_fr = dico_fr
        self.stop_en = stop_word_en
        self.stop_fr = stop_word_fr
        self.english_text = False



        # detect if this article is in english or french language
        self.english_text = self.isEnglish()

        # remove stop word to process the text
        self.subject = self.removeStopWord(self.subject)
        self.message = self.removeStopWord(self.message)

        # correct wrong words in abstract
        if self.english_text:
            self.preprocess(self.stop_en, self.dico_en)
        else:
            self.preprocess(self.stop_fr, self.dico_fr)


    def removeStopWord(self, data):
        tab = []

        for w in data:
            if self.english_text:
                if w not in self.stop_en:
                    tab.append(w)
            elif w not in self.stop_fr:
                tab.append(w)
        return tab

    def isEnglish(self):
        l = len(self.message)
        english_word = 0
        french_word = 0

        for w in self.message:
            if w in self.stop_en:
                english_word += 1
            if w in self.stop_fr:
                french_word += 1
        #print("ratio french word", french_word/l, "ratio english word", english_word/l)

        return english_word/l > french_word/l

    def preprocess(self, stop_word, dico):
        strange_word = []
        insert = []
        c1, c2 = 0, 0
        shift = 0

        # search word which are not recognize
        for w in self.message:
            c2 += 1
            if len(w) > 1 and w not in dico:
                strange_word.append((w, c2))
                c1 += 1
        # print(c1, c2)

        # print("Avant", self.abstract)

        # search two new words from a detected strange word
        for (w, index) in strange_word:
            for i in range(len(w) - 1, 0, -1):
                if w[:i] in dico:
                    if w[:i] not in stop_word and w[i:] not in stop_word:
                        insert.append(w[:i])
                        insert.append(w[i:])
                        self.message = self.message[:index + shift - 1] + insert + self.message[index + shift:]
                        shift += 1
                    elif w[:i] not in stop_word and w[i:] in stop_word:
                        insert.append(w[:i])
                        self.message = self.message[:index + shift - 1] + insert + self.message[index + shift:]
                    elif w[:i] in stop_word and w[i:] not in stop_word:
                        insert.append(w[i:])
                        self.message = self.message[:index + shift - 1] + insert + self.message[index + shift:]
                    elif w[:i] in stop_word and w[i:] in stop_word:
                        self.message = self.message[:index + shift - 1] + self.message[index + shift:]
                        shift -= 1
                    insert = []
                    break

