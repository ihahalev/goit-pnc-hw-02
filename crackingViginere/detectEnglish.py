# Detect English module
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)
# To use, type this code:
#   import detectEnglish
#   detectEnglish.isEnglish(someString) # Returns True or False
# (There must be a "dictionary.txt" file in this directory with all
# English words in it, one word per line. You can download this from
# https://www.nostarch.com/crackingcodes/.)
from pathlib import Path

UPPERLETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_AND_SPACE = UPPERLETTERS + UPPERLETTERS.lower() + ' \t\n'
def loadDictionary():
    crack_folder = "crackingViginere"
    if crack_folder not in str(Path.cwd()):
        crack_path = Path.cwd()/crack_folder
    else:
        crack_path = Path.cwd()
    dictionaryFile = open(str(crack_path/'dictionary.txt'))
    englishWords = {}
    for word in dictionaryFile.read().split('\n'):
        englishWords[word] = None
    dictionaryFile.close()
    return englishWords
ENGLISH_WORDS = loadDictionary()
def getEnglishCount(message):
    message = message.upper()
    message = removeNonLetters(message)
    possibleWords = message.split()
    if possibleWords == []:
        return 0.0 # No words at all, so return 0.0
    matches = 0
    for word in possibleWords:
        if word in ENGLISH_WORDS:
            matches += 1
    return float(matches) / len(possibleWords)
def removeNonLetters(message):
    lettersOnly = []
    for symbol in message:
        if symbol in LETTERS_AND_SPACE:
            lettersOnly.append(symbol)
    return ''.join(lettersOnly)
def isEnglish(message, wordPercentage=20, letterPercentage=85):
    # By default, 20% of the words must exist in the dictionary file, and
    # 85% of all the characters in the message must be letters or spaces
    # (not punctuation or numbers).
    wordsMatch = getEnglishCount(message) * 100 >= wordPercentage
    numLetters = len(removeNonLetters(message))
    messageLettersPercentage = float(numLetters) / len(message) * 100
    lettersMatch = messageLettersPercentage >= letterPercentage
    return wordsMatch and lettersMatch

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

if __name__ == "__main__":
    text = read_file('plain_text.txt')
    print(isEnglish(text))