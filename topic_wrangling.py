import pandas
import re

def main():
	df = pandas.read_csv("metoo_d3.csv")
	lexicon = pandas.read_csv("SentiWords_1.1.csv")
	
	# sub out #s
	lexicon['word'] = [re.sub(r"#\D", "", word) for word in lexicon['word']]

	# filter only topic 1
	df = df[df['topic'] == 1]
	s = df['count'].sum()
	df['prop'] = df['count'].apply(lambda g: g/s)
	
	# join two datasets
	df = pandas.merge(df, lexicon, on='word', how='left')

	# filter out null values
	df = df[df['score'].notnull()]

	# convert to csv
	df.to_csv("metoo_topic_1.csv")

main()