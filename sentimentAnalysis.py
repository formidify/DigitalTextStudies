import nltk
import csv
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def main():
	with open("136598840398995_facebook_statuses.csv") as file:

		sum = 0
		compound = 0
		pos = 0
		neg = 0
		neu = 0

		reader = csv.DictReader(file, delimiter = ',')
		sid = SentimentIntensityAnalyzer()

		for row in reader:
			line = row['status_message']
			print(line)

			ss = sid.polarity_scores(line)
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


if __name__ == '__main__':
	main()