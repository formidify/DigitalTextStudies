# ngrams.py
# James Yang
# program used to generate n-gram counts for the data of #metoo posts
# some of the methods originally written by Eric Alexander and modified

import csv
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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

        # Get stopwords
        with open("stopwords.txt") as f:
            stopwords = [word for line in f for word in line.split()]

        # Add to oneGramCounts for each word
        for word in words:
            if word not in stopwords:
                oneGramCounts[word] = oneGramCounts.get(word, 0) + 1

    return oneGramCounts

def getOneGrams_subset(reader):
    oneGramCounts = {}
    sid = SentimentIntensityAnalyzer()
    sum = 0
    for row in reader:
        line = row['status_message']

        ss = sid.polarity_scores(line)

        if ss['compound'] <= 0.2 and ss['compound'] >= -0.2: # specifies what values of compound to keep
            sum = sum + 1
            for ch in '!@#$%^&*()_+-=;:",./<>?\\':
                line = line.replace(ch, ' ')
        
            line = line.lower()
            
            words = line.split()

            # Get stopwords
            with open("stopwords.txt") as f:
                stopwords = [word for line in f for word in line.split()]

            for word in words:
                if word not in stopwords:
                    oneGramCounts[word] = oneGramCounts.get(word, 0) + 1

    print(sum)
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
        
        '''
        # Take care of numbers
        data = nltk.pos_tag(words)

        
        for i in range(len(data)):
            if 'CD' in data[i][1]:
                words[i] = 'num'
        '''
        # Get stopwords
        with open("stopwords.txt") as f:
            stopwords = [word for line in f for word in line.split()]

        # Add to twoGramCounts for each word
        i = 0
        for i in range(len(words) - 1):
            # the case when phrases with both stopwords are excluded
            # if not (words[i] in stopwords and words[i+1] in stopwords):

            # the case when only phrases with both non-stopwords are included
            if words[i] not in stopwords and words[i+1] not in stopwords:
                word = words[i] + ' ' + words[i+1]
                twoGramCounts[word] = twoGramCounts.get(word, 0) + 1

    return twoGramCounts

def getTwoGrams_subset(reader):
    twoGramCounts = {}
    sid = SentimentIntensityAnalyzer()

    for row in reader:
        line = row['status_message']

        ss = sid.polarity_scores(line)

        if ss['compound'] <= 0.2 and ss['compound'] >= -0.2: # specifies what values of compound to keep

            for ch in '!@#$%^&*()_+-=;:",./<>?\\':
                line = line.replace(ch, ' ')
            
            while '  ' in line:
                line = line.replace('  ', ' ')
            
            line = line.lower()
            
            words = line.split()
            
            # Get stopwords
            with open("stopwords.txt") as f:
                stopwords = [word for line in f for word in line.split()]

            i = 0
            for i in range(len(words) - 1):
                # the case when phrases with both stopwords are excluded
                if not (words[i] in stopwords and words[i+1] in stopwords):

                # the case when only phrases with both non-stopwords are included
                # if words[i] not in stopwords and words[i+1] not in stopwords:
                    word = words[i] + ' ' + words[i+1]
                    twoGramCounts[word] = twoGramCounts.get(word, 0) + 1

    return twoGramCounts


'''
Identifies n-grams for words with a given range of compound values
'''

def getNGrams_subset(reader, n):
    ''' Function takes in a given text filename and an integer n and counts n-grams in the file '''
    nGramCounts = {}
    sid = SentimentIntensityAnalyzer()
    sum = 0 # how many posts in a category given compound value

    for row in reader:

        line = row['status_message']

        ss = sid.polarity_scores(line)


        if ss['compound'] <= 1 and ss['compound'] >= 0.8: # specifies what values of compound to keep
            sum = sum + 1
            for ch in '!@#$%^&*()_+-=;:",./<>?\\':
                line = line.replace(ch, ' ')
            
            while '  ' in line:
                line = line.replace('  ', ' ')
            
            line = line.lower()
            
            words = line.split()

            data = nltk.pos_tag(words)

            for i in range(len(data)):
                if 'CD' in data[i][1]:
                    words[i] = 'num'
                # if words[i] in stopwords:
                    # words.remove(words[i])
            
            i = 0
            for i in range(len(words) - n + 1):
                sublist = words[i:i+n]
                j = 0
                word = ''
                for j in range(len(sublist)):
                    word += sublist[j] + ' '
                nGramCounts[word] = nGramCounts.get(word, 0) + 1

    print(sum)
    return nGramCounts


def getNGrams(reader, n):
    nGramCounts = {}
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
            # if words[i] in stopwords:
                # words.remove(words[i])
        
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
    
    # calculate average
    # sum = 0
    for i in range(n):
        word, count = dictItems[i]
        print('{} {}'.format(word, count))
        # add average
        # sum += count
    # print("The average of the first", n, "words is ", sum/n)

def main():
    with open("136598840398995_facebook_statuses.csv") as file:
        reader = csv.DictReader(file, delimiter = ',')
        n = int(input("How many grams? "))
        display = int(input("How many to display? "))
        
        if n == 1:
            nGrams = getOneGrams_subset(reader)
        elif n == 2:
            nGrams = getTwoGrams_subset(reader)
        else: 
            nGrams = getNGrams_subset(reader, n)

        printTopN(nGrams, display)


if __name__ == '__main__':
    main()
