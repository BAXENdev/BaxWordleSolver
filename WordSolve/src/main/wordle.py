
import word_filter as wf
import random

class Wordle():
    def __init__(self, wordListPath):
        self.wf = wf.WordFilter()
        self.word = None
        self.table = list()
        
    def newGame(self, guessCount=None, wordSize=None):
        if guessCount:
            self.guessCount = guessCount
        else:
            self.guessCount = 6
        # if wordSize:
        #     self.wordSize = wordSize
        # else
        self.word = random.choice(self.wf.get_all_words())
        

