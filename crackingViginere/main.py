# Vigenere Cipher Hacker
# https://www.nostarch.com/crackingcodes/ (BSD Licensed)

import itertools, re
import pyperclip, freqAnalysis, detectEnglish as detectEnglish

vigenere = __import__('vigenere')
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
MAX_KEY_LENGTH = 16 # Will not attempt keys longer than this.
NUM_MOST_FREQ_LETTERS = 26 # Attempt this many letters per subkey.
SILENT_MODE = False # If set to True, program doesn't print anything.
NONLETTERS_PATTERN = re.compile('[^A-Z]')

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    # Instead of typing this ciphertext out, you can copy & paste it
    # from https://www.nostarch.com/crackingcodes/:
    ciphertext = """Adiz Avtzqeci Tmzubb wsa m Pmilqev halpqavtakuoi,
        lgouqdaf, kdmktsvmztsl, izr xoexghzr kkusitaaf. Vz wsa twbhdg
        ubalmmzhdad qz
        --snip--
        azmtmd'g widt ion bwnafz tzm Tcpsw wr Zjrva ivdcz eaigd yzmbo
        Tmzubb a kbmhptgzk dvrvwz wa efiohzd."""
    text = read_file('plain_text.txt')
    key_encr = "CRYPTOGRAPHY"
    ciphertext = vigenere.vigenere_encrypt(text, key_encr)

    hackedMessage = hackVigenere(ciphertext)
    if hackedMessage != None:
        print('Copying hacked message to clipboard:')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
    else:
        print('Failed to hack encryption.')
def findRepeatSequencesSpacings(message: str):
    # Goes through the message and finds any 3- to 5-letter sequences
    # that are repeated. Returns a dict with the keys of the sequence and
    # values of a list of spacings (num of letters between the repeats).
    # Use a regular expression to remove non-letters from the message:
    message = NONLETTERS_PATTERN.sub('', message.upper())
    # Compile a list of seqLen-letter sequences found in the message:
    seqSpacings = {} # Keys are sequences; values are lists of int spacings.
    for seqLen in range(3, 6):
        for seqStart in range(len(message) - seqLen):
            # Determine what the sequence is and store it in seq:
            seq = message[seqStart:seqStart + seqLen]
            # Look for this sequence in the rest of the message:
            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    # Found a repeated sequence:
                    if seq not in seqSpacings:
                        seqSpacings[seq] = [] # Initialize blank list.
                    # Append the spacing distance between the repeated
                    # sequence and the original sequence:
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings
def getUsefulFactors(num: int):
    # Returns a list of useful factors of num. By "useful" we mean factors
    # less than MAX_KEY_LENGTH + 1 and not 1. For example,
    # getUsefulFactors(144) returns [2, 3, 4, 6, 8, 9, 12, 16].
    if num < 2:
        return [] # Numbers less than 2 have no useful factors.
    factors = [] # The list of factors found.
    # When finding factors, you only need to check the integers up to
    # MAX_KEY_LENGTH:
    for i in range(2, MAX_KEY_LENGTH + 1): # Don't test 1: it's not useful.
        if num % i == 0:
            factors.append(i)
            otherFactor = int(num / i)
            if otherFactor < MAX_KEY_LENGTH + 1 and otherFactor != 1:
                factors.append(otherFactor)
    return list(set(factors)) # Remove duplicate factors.
def getItemAtIndexOne(x):
    return x[1]
def getMostCommonFactors(seqFactors):
    # First, get a count of how many times a factor occurs in seqFactors:
    factorCounts = {} # Key is a factor; value is how often it occurs.
    # seqFactors keys are sequences; values are lists of factors of the
    # spacings. seqFactors has a value like {'GFD': [2, 3, 4, 6, 9, 12,
    # 18, 23, 36, 46, 69, 92, 138, 207], 'ALW': [2, 3, 4, 6, ...], ...}.
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1
    # Second, put the factor and its count into a tuple and make a list
    # of these tuples so we can sort them:
    factorsByCount = []
    for factor in factorCounts:
        # Exclude factors larger than MAX_KEY_LENGTH:
        if factor <= MAX_KEY_LENGTH:
            # factorsByCount is a list of tuples: (factor, factorCount).
            # factorsByCount has a value like [(3, 497), (2, 487), ...].
            factorsByCount.append( (factor, factorCounts[factor]) )
    # Sort the list by the factor count:
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)
    return factorsByCount
def kasiskiExamination(ciphertext):
    # Find out the sequences of 3 to 5 letters that occur multiple times
    # in the ciphertext. repeatedSeqSpacings has a value like
    # {'EXG': [192], 'NAF': [339, 972, 633], ... }:
    repeatedSeqSpacings = findRepeatSequencesSpacings(ciphertext)
    # (See getMostCommonFactors() for a description of seqFactors.)
    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getUsefulFactors(spacing))
    # (See getMostCommonFactors() for a description of factorsByCount.)
    factorsByCount = getMostCommonFactors(seqFactors)
    # Now we extract the factor counts from factorsByCount and
    # put them in allLikelyKeyLengths so that they are easier to
    # use later:
    allLikelyKeyLengths = []
    for twoIntTuple in factorsByCount:
        allLikelyKeyLengths.append(twoIntTuple[0])
    return allLikelyKeyLengths
def getNthSubkeysLetters(nth: str, keyLength: int, message: str):
    # Returns every nth letter for each keyLength set of letters in text.
    # E.g. getNthSubkeysLetters(1, 3, 'ABCABCABC') returns 'AAA'
    #      getNthSubkeysLetters(2, 3, 'ABCABCABC') returns 'BBB'
    #      getNthSubkeysLetters(3, 3, 'ABCABCABC') returns 'CCC'
    #      getNthSubkeysLetters(1, 5, 'ABCDEFGHI') returns 'AF'
    # Use a regular expression to remove non-letters from the message:
    message = NONLETTERS_PATTERN.sub('', message.upper())
    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)
def attemptHackWithKeyLength(ciphertext: str, mostLikelyKeyLength: int):
    # Determine the most likely letters for each letter in the key:
    ciphertextUp = ciphertext.upper()
    # allFreqScores is a list of mostLikelyKeyLength number of lists.
    # These inner lists are the freqScores lists:
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertextUp)
        # freqScores is a list of tuples like
        # [(<letter>, <Eng. Freq. match score>), ... ]
        # List is sorted by match score. Higher score means better match.
        # See the englishFreqMatchScore() comments in freqAnalysis.py.
        freqScores = []
        for possibleKey in LETTERS:
            decryptedText = vigenere.vigenere_decrypt(nthLetters, possibleKey)
            keyAndFreqMatchTuple = (possibleKey, freqAnalysis.englishFreqMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)
        # Sort by match score:
        freqScores.sort(key=getItemAtIndexOne, reverse=True)
        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])
    if not SILENT_MODE:
        for i in range(len(allFreqScores)):
            # Use i + 1 so the first letter is not called the "0th" letter:
            print('Possible letters for letter %s of the key: ' % (i + 1), end='')
            for freqScore in allFreqScores[i]:
                print('%s ' % freqScore[0], end='')
            print() # Print a newline.
    # Try every combination of the most likely letters for each position
    # in the key:
    input("> ")
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        # Create a possible key from the letters in allFreqScores:
        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]
        if not SILENT_MODE:
            print('Attempting with key: %s' % (possibleKey))
        decryptedText = vigenere.vigenere_decrypt(ciphertextUp, possibleKey)
        if possibleKey == "CRYPTOGRAPHY":
            print(decryptedText)
            print(detectEnglish.isEnglish(decryptedText))
            input("> ")
        if detectEnglish.isEnglish(decryptedText):
            # Set the hacked ciphertext to the original casing:
            input("English > ")
            origCase = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = ''.join(origCase)
            # Check with user to see if the key has been found:
            print('Possible encryption hack with key %s:' % (possibleKey))
            print(decryptedText[:200]) # Only show first 200 characters.
            print()
            print('Enter D if done, anything else to continue hacking:')
            response = input('> ')
            if response.strip().upper().startswith('D'):
                return decryptedText
    # No English-looking decryption found, so return None:
    return None
def hackVigenere(ciphertext):
    # First, we need to do Kasiski examination to figure out what the
    # length of the ciphertext's encryption key is:
    allLikelyKeyLengths = sorted(kasiskiExamination(ciphertext))
    if not SILENT_MODE:
        keyLengthStr = ''
        for keyLength in allLikelyKeyLengths:
            keyLengthStr += '%s ' % (keyLength)
        print('Kasiski examination results say the most likely key lengths are: ' + keyLengthStr + '\n')
        input("> ")
    hackedMessage = None
    for keyLength in allLikelyKeyLengths:
        if not SILENT_MODE:
            print('Attempting hack with key length %s (%s possible keys)...'
              % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
        if hackedMessage != None:
            break
    # If none of the key lengths found using Kasiski examination
    # worked, start brute-forcing through key lengths:
    if hackedMessage == None:
        if not SILENT_MODE:
            print('Unable to hack message with likely key length(s). Brute-forcing key length...')
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            # Don't recheck key lengths already tried from Kasiski:
            if keyLength not in allLikelyKeyLengths:
                if not SILENT_MODE:
                    print('Attempting hack with key length %s (%s possiblekeys)...' % (keyLength, NUM_MOST_FREQ_LETTERS **keyLength))
                hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
                if hackedMessage != None:
                    break
    return hackedMessage
# If vigenereHacker.py is run (instead of imported as a module), call
# the main() function:
if __name__ == '__main__':
    main()