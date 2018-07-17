import os
import sys
import csv

def main():
	file = open(sys.argv[1]) # such as scores_tweets.csv

	file_path = "./mallet/data/tweets"
	os.mkdir(file_path)

	reader = csv.DictReader(file, delimiter = ',')
	a = 0
	for row in reader:
		line = row['line']
		name = os.path.join(file_path, str(a) + ".txt")
		txt_file = open(name,"w+")
		txt_file.write(line) 
		txt_file.close()
		a = a+1
main()