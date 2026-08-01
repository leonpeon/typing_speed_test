from random import choice

class Words():
    def __init__(self):
        with open("word_list.txt") as file:
            self.word_list = file.readlines()
        self.words_for_test = self.test_words()

    def test_words(self):
        word_list = []
        while len(word_list) < 200:
            word = choice(self.word_list).strip()
            if word not in word_list:
                word_list.append(word)
        self.words_for_test = word_list
        return word_list