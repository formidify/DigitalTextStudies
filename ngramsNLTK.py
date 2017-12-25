import csv
import operator
import nltk

def main():
	with open("136598840398995_facebook_statuses.csv") as file:
		reader = csv.DictReader(file, delimiter = ',')
		corpus = ''
		fdist = []
		for row in reader:
			line = row['status_message']
			for ch in '!@#$%^&*()_+-=;:",./<>?\\':
				line = line.replace(ch, ' ')
			tokens = nltk.word_tokenize(line)
			ngs = nltk.ngrams(tokens, 4)
			fdist += ngs
		fdist = nltk.FreqDist(fdist)
		fdist = fdist.most_common(50)
		for i in range(50):
			word= fdist[i][0]
			count = fdist[i][1]
			print('{} {}'.format(word, count))

if __name__ == '__main__':
	main()
