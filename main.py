import glob
import re
import string
import operator

#each letter/number corresponds to a prime number
lookupTable = {'a': 2, 'b': 3, 'c': 5, 'd': 7, 'e': 11, 'f': 13, 'g': 17, 'h': 19, 'i': 23, 'j': 29, 'k': 31, 'l': 37,
               'm': 41, 'n': 43, 'o': 47, 'p': 53, 'q': 59, 'r': 61, 's': 67, 't': 71, 'u': 73, 'v': 79, 'w': 83,
               'x': 89, 'y': 97, 'z': 101, ' ': 103, '1': 107, '2': 109, '3': 113, '4': 127, '5': 131, '6': 137,
               '7': 139, '8': 149, '9': 151, '0': 157}
#any explicit words can be placed here
curse_words = ['explicit words here']


def alpha_to_prime(char):
    if char in lookupTable.keys():
        return float(lookupTable[char])
    else:
        return 1

#recursive call to feed each letter of string to alpha_to_prime
def string_to_hash(to_hash):
    if len(to_hash) == 1:
        return float(alpha_to_prime(to_hash))
    else:
        return float(alpha_to_prime(to_hash[0]) * string_to_hash(to_hash[1:]))

#defines each class
class Stats:
    def __init__(self):
        self.words = 0
        self.sentences = 0
        self.lines = 0
        self.anagrams = {}
        self.frequency = {}
        self.punctuation_frequency = {}
        self.explicit = False

#checks the explicit words & anagrams
    def addword(self, word):
        self.words += 1
        clean_word = str(word).lower()
        if clean_word in curse_words:
            self.explicit = True
        if clean_word in self.frequency.keys():
            self.frequency[clean_word] += 1
        else:
            self.frequency[clean_word] = 1
        hashed_string = string_to_hash(clean_word)
        hashed_string_string = str(hashed_string)
        if hashed_string_string in self.anagrams.keys():
            if clean_word not in self.anagrams[hashed_string_string]:
                self.anagrams[hashed_string_string].append(clean_word)
        else:
            self.anagrams[hashed_string_string] = [clean_word]

    def ingestline(self, line):
        p = re.compile(r"\w+(?:'\w+)*|[^\w\s]")
        items = p.findall(line)
        self.lines += 1
        for item in items:
            if not item.isdigit() and item not in string.punctuation and item != '\'':
                self.addword(item)
            if item in string.punctuation:
                if item in self.punctuation_frequency.keys():
                    self.punctuation_frequency[item] += 1
                else:
                    self.punctuation_frequency[item] = 1
                if item in ['.', '!', '?']:
                    self.sentences += 1

    def ingestfile(self, file):
        with open(file) as fp:
            line = fp.readline()
            while line:
                self.ingestline(line)
                line = fp.readline()
        self.cleananagram()

    def cleananagram(self):
        temp_anagram_array = []
        for key in self.anagrams.keys():
            if len(self.anagrams[key]) > 1:
                temp_anagram_array.append(self.anagrams[key])
        self.anagrams = temp_anagram_array

#data is printed
    def __str__(self):
        return_string = ''
        if self.explicit:
            return_string += 'Text is explicit. \n'
        else:
            return_string += 'Text is probably not explicit. \n'
        return_string += "Number of words: " + str(self.words) + '\n'
        return_string += "Number of sentences: " + str(self.sentences) + '\n'
        return_string += "Number of lines: " + str(self.lines) + '\n'
        if self.punctuation_frequency != {}:
            return_string += "Punctuation frequency: " + str(self.punctuation_frequency) + '\n'
            return_string += "Most frequent punctuation: " + str(
                max(self.punctuation_frequency.items(), key=operator.itemgetter(1))[0]) + '\n'
        return_string += "Most frequent word: " + str(max(self.frequency.items(), key=operator.itemgetter(1))[0]) + '\n'
        if self.anagrams:
            return_string += "Anagrams: \n"
            for item in self.anagrams:
                return_string += ','.join(item) + '\n'
        return return_string


#checks folder for available files
def get_file():
    files = glob.glob("*.txt")
    print("Available files: ")
    number = 1
    for file in files:
        print(str(number) + ": " + file)
        number += 1
    file_number = "-1"
    while not file_number.isdigit():
        file_number = input("File number to read: ")
    if not len(files) >= int(file_number) > 0:
        print("Out of scope of files.")
        return
    else:
        return files[int(file_number) - 1]


#def test(to_test):
    #print(to_test + ": " + str(string_to_hash(to_test)))


if __name__ == '__main__':
    start = Stats()
    while glob.glob("*.txt"):
        start = Stats()
        start.ingestfile(get_file())
        print(start)
    exit("No text files found, please place text files in this directory")
