# ngrams.py
# James Yang
# program used to generate n-gram counts for the data of #metoo posts
# some of the methods originally written by Eric Alexander and modified

import csv
import nltk

''' Function takes in a given text filename and counts one-grams in the file '''
def getOneGrams(reader):
    oneGramCounts = {}
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

def getTwoGrams(reader):
    ''' Function takes in a given text filename and returns 2-grams for the given text '''
    twoGramCounts = {}
    #reader = csv.DictReader(filename, delimiter = ',')
    for row in reader:
        line = row['status_message']
        # Clean out punctuation
        for ch in '!@#$%^&*()_+-=;:",./<>?\\':
            line = line.replace(ch, ' ')
        
        while '  ' in line:
            line = line.replace('  ', ' ')
        
        # Reduce to all lowercase
        line = line.lower()
        
        # Split into words
        words = line.split()
        
        # Take care of numbers
        data = nltk.pos_tag(words)

        for i in range(len(data)):
            if 'CD' in data[i][1]:
                words[i] = 'num'

        # Add to twoGramCounts for each word
        i = 0
        for i in range(len(words) - 1):
            word = words[i] + ' ' + words[i+1]
            #print(word)
            twoGramCounts[word] = twoGramCounts.get(word, 0) + 1

    return twoGramCounts

def getNGrams(reader, n):
    ''' Function takes in a given text filename and an integer n and counts n-grams in the file '''
    nGramCounts = {}
    #reader = csv.DictReader(filename, delimiter = ',')
    for row in reader:
        line = row['status_message']
        # Clean out punctuation
        for ch in '!@#$%^&*()_+-=;:",./<>?\\':
            line = line.replace(ch, ' ')
        
        while '  ' in line:
            line = line.replace('  ', ' ')
        
        # Reduce to all lowercase
        line = line.lower()
        
        # Split into words
        words = line.split()

        # Take care of numbers
        data = nltk.pos_tag(words)

        for i in range(len(data)):
            if 'CD' in data[i][1]:
                words[i] = 'num'
        
        # Add to twoGramCounts for each word
        i = 0
        for i in range(len(words) - n + 1):
            sublist = words[i:i+n]
            j = 0
            word = ''
            for j in range(len(sublist)):
                word += sublist[j] + ' '
            nGramCounts[word] = nGramCounts.get(word, 0) + 1

    return nGramCounts

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
        reader = csv.DictReader(file, delimiter = ',')
        #oneGrams = getOneGrams(reader)
        #printTopN(oneGrams, 50)
        #twoGrams = getTwoGrams(reader)
        #printTopN(twoGrams, 50)
        nGrams = getNGrams(reader, 1)
        printTopN(nGrams, 550)


if __name__ == '__main__':
    main()
