
from colorama import init
init()
import sys

letter_block_size, letter_count_block_size, word_count_block_size = 12, 40, 40

def letter_block(string):
    ret = f'Letter "{string}"'
    space = letter_block_size - len(ret)
    ret += " " * space
    return ret

def letter_count_block(count, total):
    ret = f'Count = {str(count)} ; Percent = {"{:.02f}".format((count/total)*100)}'
    space = letter_count_block_size - len(ret)
    ret += " " * space
    return ret

def word_count_block(count, total):
    ret = f'Count = {str(count)} ; Percent = {"{:.02f}".format((count/total)*100)}'
    space = letter_count_block_size - len(ret)
    ret += " " * space
    return ret

letter_block("a")

fr = open("./WordSolve/_5_letter_words_sorted.txt", "r")
# fw = open("./word_stats/word_stats.txt", "w")
# sys.stdout = fw 

words = fr.read().split("\n")
fr.close()
# words.remove("\n")

letters = "abcdefghijklmnopqrstuvwxyz"
occurrances = list()
for letter in letters:
    letter_count = 0
    word_count = 0
    for word in words:
        c = word.count(letter)
        if c > 0:
            word_count += 1
            letter_count += c
        
    occurrances.append((letter, letter_count, word_count))

stats = list()
word_size = len(words)
letter_size = word_size * 5
print(f"Letter{' ' * (letter_block_size - 6)} | Letter count & percent of all letters{' ' * (letter_count_block_size - 37)} | Word count & percent of all words{' ' * (word_count_block_size - 33)}")
print(f"Total{' ' * (letter_block_size - 5)} | Letter total = {str(letter_size)}{' ' * (letter_count_block_size - 15 - len(str(letter_size)))} | Word total = {str(word_size)}{' ' * (word_count_block_size - 13 - len(str(word_size)))}")
for (letter, letter_count, word_count) in occurrances:
    print(f"{letter_block(letter)} | {letter_count_block(letter_count, letter_size)} | {word_count_block(word_count, word_size)}")

# fw.close
