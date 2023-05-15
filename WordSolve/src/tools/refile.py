
class Word():
    def __init__(self, word: str) -> None:
        # Initialize Word.word
        self.word = word.lower()
        
        # Initialize Word.letter_values
        self.letter_values = [ord(letter) for letter in self.word]
        
        # Initialize Word.word_value
        self.word_value = 0
        letter_values = self.letter_values.copy()
        letter_values.reverse()
        for i, value in zip(range(len(letter_values)), letter_values):
            self.word_value += value << (i * 8)
    
    # Less Than operator overload
    def __lt__(self, other) -> bool:
        return self.word_value < other.word_value
    
    # Greater Than operator overload
    def __gt__(self, other) -> bool:
        return self.word_value > other.word_value

    # Str operator overload
    def __str__(self) -> str:
        return f"Word({self.word}, {self.word_value}, {self.letter_values})"

# Open files
f_read = open("./WordSolve/5_letter_words.txt", "r")
f_write = open("./WordSolve/sorted_5_letter_words.txt", "w")

# Sort words
words = [Word(word) for word in f_read.read().split("\n")]
words.sort()
for w in words:
    f_write.write(w.word + "\n")

# Close files
f_read.close()
f_write.close()
