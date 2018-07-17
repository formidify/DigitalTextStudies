import nltk
import csv
import sys
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def parse_sentiment(file, myfile):
	sum = 0
	compound = 0
	pos = 0
	neg = 0
	neu = 0

	reader = csv.DictReader(file, delimiter = ',')
	sid = SentimentIntensityAnalyzer()
	writer = csv.writer(myfile)
	writer.writerow(["neg", "neu", "pos", "compound", "line"])
	for row in reader:
		line = row['status_message']

		# These pre-processing replacements are for the tweets dataset specifically
		line = line.replace('@anonymous', '')
		line = line.replace('http://url_removed', '')
		line = line.replace('&amp', '')
		
		print(line)

		ss = sid.polarity_scores(line)
		writer.writerow([ss['neg'], ss['neu'], ss['pos'], ss['compound'], line])

		for k in ss:
			print('{0}: {1}, '.format(k, ss[k]), end='')
		print()
		
		sum += 1
		neg += ss['neg']
		neu += ss['neu']
		pos += ss['pos']
		compound += ss['compound']
		

	print('The average of neg is {0}.'.format(neg/sum))
	print('The average of neu is {0}.'.format(neu/sum))
	print('The average of pos is {0}.'.format(pos/sum))
	print('The average of compound is {0}.'.format(compound/sum))

def main():
	file = open(sys.argv[1])
	myfile = open(sys.argv[2], 'w')
	parse_sentiment(file, myfile)


if __name__ == '__main__':
	main()