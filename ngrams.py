# ngrams.py
# James Yang
# program used to generate n-gram counts for the data of #metoo posts
# some of the methods originally written by Eric Alexander and modified

import csv

''' Function takes in a given text filename and counts one-grams in the file '''
def getOneGrams(filename):
    
    oneGramCounts = {}
    reader = csv.DictReader(filename, delimiter = ',')
    for row in reader:
        line = row['status_message']
        # Clean out punctuation
        for ch in '!@#$%^&*()_+-=;:",./<>?\\':
            line = line.replace(ch, ' ')
    
        # Reduce to all lowercase
        line = line.lower()
        
        # Split into words
        words = line.split()
        
        # Add to oneGramCounts for each word
        for word in words:
            oneGramCounts[word] = oneGramCounts.get(word, 0) + 1

    return oneGramCounts

def byCount(pair):
    ''' Helper function to let printTopN() sort (n-gram, count) tuples. '''
    return pair[1]

def printTopN(countDict, n):
    ''' Function takes a dictionary mapping n-grams to counts and prints top n n-grams by count. '''
    
    dictItems = list(countDict.items())
    dictItems.sort()
    dictItems.sort(key=byCount, reverse=True)
    
    for i in range(n):
        word, count = dictItems[i]
        print('{} {}'.format(word, count))

def main():
    with open("136598840398995_facebook_statuses.csv") as file:
        oneGrams = getOneGrams(file)
        printTopN(oneGrams, 50)


if __name__ == '__main__':
    main()
