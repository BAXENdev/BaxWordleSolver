
from typing import Callable, Iterable
import sys

FIVE_LETTER_LIST_PATH = "./WordSolve/_5_letter_words_sorted.txt"

# Functions

def read_words(filepath) -> list[str]:
    f = open(filepath, "r")
    s = f.read().split("\n")
    for i in range(s.count('')):
        s.remove('')
    f.close()
    return [Word(w) for w in s]

def foldr(func, base_case, list):
    if len(list) == 0:
        return base_case
    
    acc = base_case
    for element in list:
        acc = func(acc, element)
    
    return acc

def FilterRegex(*regexs: str):
    """Custom regex for generating filters
    [verb][letter] x5, ....
    verb = { n = Not here, inclusive of y | z = Not in word at all | y = In word but not here | g = Here, but there may be more }
    letter = letter (duh)

    Returns:
        LettersAreHere, LettersAreNotHere, LettersAreInWord, LettersAreNotInWord
    """
    def splitWord(word: str):
        letterCases = list()
        length = len(word)
        # Assume length is even
        for i in range(length // 2):
            letterCase = word[i * 2] + word[i * 2 + 1]
            letterCases += [letterCase]
        return letterCases

    def addUnique(l: list, e):
        if e not in l:
            return l + [e]
        else:
            return l

    lettersAreHere = list()
    lettersArentHere = list()
    lettersAreInWord = list()
    lettersArentInWord = list()

    for regex in regexs:
        cases = splitWord(regex)
        for i in range(len(cases)):
            verb, letter = cases[i].lower()
            if verb == "_" or letter == "_":
                continue
            if verb == "n":
                lettersArentHere = addUnique(lettersArentHere, (letter, i))
            elif verb == "z":
                lettersArentInWord = addUnique(lettersArentInWord, letter)
            elif verb == "y":
                lettersAreInWord = addUnique(lettersAreInWord, letter)
                lettersArentHere = addUnique(lettersArentHere, (letter, i))
            elif verb == "g":
                lettersAreHere = addUnique(lettersAreHere, (letter, i))
            elif verb == "h":
                lettersAreInWord = addUnique(lettersAreInWord, letter)
    
    return LettersAreHere(lettersAreHere), LettersAreNotHere(lettersArentHere), \
        LettersAreInWord(lettersAreInWord), LettersAreNotInWord(lettersArentInWord)
            

# Classes

class WordFilter():
    def __init__(self, filepath=None) -> None:
        if not filepath:
            filepath = FIVE_LETTER_LIST_PATH
        self.original_words = read_words(filepath)
        self.current_words = self.original_words
        self.filters = list()
    
    def reset_words(self):
        """Changes the current list to the original list that contained all words.
        """
        self.current_words = self.original_words
        self.filters = list()
    
    def reduce_list(self, *filters: filter):
        """Removes any words that do not match the filters given.

        Paramaters:
        filters: a list of functions that accept one Word as a parameter and returns a boolean.
        """
        def flatten(items):
            if not issubclass(type(items), Iterable):
                return [items]
            ret = list()
            for i in items:
                ret += flatten(i)
            return ret
        
        # Append new filters to the filters list
        # filters = flatten(filters)
        self.filters.append(filters)

        # Filter every word in the current list through the new filters
        new_list = list()
        for w in self.current_words:
            isValid = True
            for filter in filters:
                if not filter(w):
                    isValid = False
                    break
            if isValid:
                new_list.append(w)
        self.current_words = new_list
        return self.get_current_words()

    def get_all_words(self):
        return [w.word for w in self.original_words]
    
    def get_current_words(self):
        return [w.word for w in self.current_words]

    def walk_back_filter(self, steps):
        filterSize = len(self.filters)
        if steps > filterSize:
            sys.stderr.write(f"Tried walk back {steps} filters when filter only has {filterSize} filters")
            return False
        self.filters = self.filters[:filterSize - steps]
        self.reset_words()

        return True

class Word():
    def __init__(self, word: str) -> None:
        # Initialize Word.word
        self.word = word.lower()
    
    def compare_character(self, char: str, index: int):
        """Compares a given character to a character in the word.

        Parameters:
        char: the character to compare to.
        index: which character in the word being compared.
        """
        if len(char) != 1 :
            raise NotImplementedError(f"{char} is not 1 character")
        return self.word[index] == char.lower()
    
    def has_character(self, char: str):
        """Returns true if the char is in the word.

        Parameters:
        char: the character to compare to.
        """
        if len(char) != 1 :
            raise NotImplementedError(f"{char} is not 1 character")
        return self.word.count(char.lower())

    def __str__(self):
        return self.word

    def __repr__(self):
        return self.word

class Filter():
    def __init__(self, func: Callable) -> None:
        self.func = func

    def __call__(self, word: Word) -> bool:
        return self.func(word)

# Filters

class LetterIsHere(Filter):
    """Filters for words that do not have the letter at a specific index.

    Parameters:
    letter: A single chracter string that holds the character to be checked for.
    index: An integer that specifies the index to check for the character.
    """
    def __init__(self, letter: str, index: int):
        super().__init__(lambda word: word.compare_character(letter, index))

class LettersAreHere(Filter):
    """Filters for words that have any of the given letters at their given indexes.
    
    Parameters:
    lettersANDindexes: Is a list of tuples composed of (string, integer) that represents a letter and the index to check for this letter.
    EX: [("a", 0), ("g", 1)] filters for any words that start with an "a" and have a "g" as the second letter.
    """
    def __init__(self, lettersANDindexes: list[tuple[str, int]]) -> None:
        super().__init__(
            lambda word: foldr(lambda a, b: a and b, True,
                [word.compare_character(letter, index) for (letter, index) in lettersANDindexes]
            )
        )

class LetterIsNotHere(Filter):
    """Filters for words that do not have the letter at a specific index.

    Parameters:
    letter: A single chracter string that holds the character to be checked for.
    index: An integer that specifies the index to check for the character.
    """
    def __init__(self, letter: str, index: int):
        super().__init__(lambda word: not word.compare_character(letter, index))

class LettersAreNotHere(Filter):
    """Filters for words that do not have any of the given letters at their given indexes.
    
    Parameters:
    lettersANDindexes: Is a list of tuples composed of (string, integer) that represents a letter and the index to check for this letter.
    EX: [("a", 0), ("g", 1)] filters out any words that start with an "a" or have a "g" as the second letter.
    """
    def __init__(self, lettersANDindexes: list[tuple[str, int]]) -> None:
        super().__init__(
            lambda word: not foldr(lambda a, b: a or b, False,
                [word.compare_character(letter, index) for (letter, index) in lettersANDindexes]
            )
        )

class LetterIsInWord(Filter):
    """Filters for words that do have the given letter.

    Parameters:
    letter: A single chracter string that holds the character to be checked for.
    """
    def __init__(self, letter: str) -> None:
        super().__init__(lambda word: word.has_character(letter))

class LettersAreInWord(Filter):
    """Filters for words that do have any of the given letters.
    
    Parameters:
    letters: A list of single characters that represents the letters to be checked.
    """
    def __init__(self, letters: list[str]) -> None:
        super().__init__(
            lambda word: foldr(lambda a, b: a and b, True,
                [word.has_character(letter) for letter in letters]
            )
        )

class LetterIsNotInWord(Filter):
    """Filters for words that do not have the given letter.

    Parameters:
    letter: A single chracter string that holds the character to be checked for.
    """
    def __init__(self, letter: str) -> None:
        super().__init__(lambda word: not word.has_character(letter))

class LettersAreNotInWord(Filter):
    """Filters for words that do not have any of the given letters.
    
    Parameters:
    letters: A list of single characters that represents the letters to be checked.
    """
    def __init__(self, letters: list[str]) -> None:
        super().__init__(
            lambda word: not foldr(lambda a, b: a or b, False,
                [word.has_character(letter) for letter in letters]
            )
        )

class LetterHasCount(Filter):
    """Filters for words that have the given letter.
    
    Parameters:
    letter: A single chracter string that holds the character to be checked for.
    count: how many times this letter should occur.
    """
    def __init__(self, letter: str, count: int) -> None:
        super().__init__(lambda word: word.has_character(letter) == count)

class LettersHaveCount(Filter):
    """Filters for words that have the given amount of letters for each given letter.
    
    Parameters:
    lettersANDcounts: A list of tuples composed of string and integers. Ex: [("a",2),("b",1)]
    """
    def __init__(self, lettersANDcounts: list[tuple[str, int]]) -> None:
        super().__init__(
            lambda word: foldr(lambda a, b: a and b, True, 
                [word.has_character(letter) == count for (letter, count) in lettersANDcounts]
            )
        )

# main

def driver():
    ws = WordFilter()
    print("Starting WordFilter driver...")
    while True:
        i = input("Enter input: ").lower().split()

        # Crappy switch case
        if len(i) == 0:
            continue
        elif i[0] == "exit" or i[0] == "quit":
            break
        elif i[0] == "word":
            if len(i) < 2:
                print("Word requires a FilterRegex parameter.")
                continue
            if len(i[1]) % 2 != 0:
                print("FilterRegex is not even.")
                continue
            print(ws.reduce_list(FilterRegex(i[1])))
        elif i[0] == "reset":
            ws.reset_words()
            print("WordFilter reset")
        elif i[0] == "list":
            print(ws.current_words)
        elif i[0] == "listall":
            print(ws.get_all_words())
        elif i[0] == "filters":
            print(ws.filters)
        elif i[0] == "help":
            print("No help rn.")
        elif i[0] == "nothave":
            if len(i) < 2:
                print("Need a list fo letters as a parameter")
                continue
            letters = list(i[1])
            print(ws.reduce_list(LettersAreNotInWord(letters)))
        elif i[0] == "has":
            if len(i) < 2:
                print("Need a list fo letters as a parameter")
                continue
            letters = list(i[1])
            print(ws.reduce_list(LettersAreInWord(letters)))
        elif i[0] == "walkback":
            if len(i) < 2:
                print("Need a number of how many steps to walk back")
                continue
            steps = int(i[1])
            if ws.walk_back_filter(steps):
                print("List was walked back")
            else:
                print("To many steps when walking back")            
        else: # Bad input
            print("Bad input")
    
    print("Driver session ended.")

driver()
