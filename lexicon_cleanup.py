import pandas
import re

def main():
	lexicon = pandas.read_csv("SentiWords_1.1.csv", encoding='utf-8-sig')

	## cleaning the words
	# sub out #s
	def sub(word):
		word = re.sub(r"#\D", "", word)
		word = re.sub(r"_", " ", word)
		return word

	lexicon['word'] = [sub(word) for word in lexicon['word']]

	# group by and calculate mean for words
	lexicon = lexicon.groupby('word').mean().reset_index()
	
	lexicon.to_csv("SentiWords_cleaned.csv", encoding='utf-8-sig', index=False)

main()