from random import choice

class Words():
    def __init__(self):
        with open("word_list.txt") as file:
            self.word_list = file.readlines()
        self.words_for_test = self.test_words()

    def test_words(self):
        word_list = []
        while len(word_list) < 200:
            word = choice(self.word_list)
            if word in word_list:
                pass
            else:
                word_list.append(word.strip())
        return word_list