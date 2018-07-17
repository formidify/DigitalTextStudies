import sys

import pandas as pd 

'''
Find the expected sentiment for topic t by calculating the sum_t(p_d(t) * v(d)) for every document d
given the valence of the document v(d) and the document-topic proportion p_d(t). Add two columns to the
existing data_stars.csv dataset, where one can either normalize the above sum by dividing the number of 
documents ("n(d)") or by sum_t(p_d(t)) for each t. 
'''

def expectedSen(d_t, d, method):
	n_topics = len(d_t.columns) - 2
	n_docs = len(d_t.index)

	l = [0 for i in range(n_topics)]
	l2 = [0 for i in range(n_topics)]

	for index, row in d.iterrows():
		for i in range(n_topics):
			prop = d_t.loc[index,i+2]
			l[i] += prop * d.loc[index, 'compound']
			l2[i] += prop

	# print(l)

	if method == "n(d)":
	# option 1: divide every element by the number of documents in the corpus
		l = [l[i]/n_docs for i in range(n_topics)]

	if method == "d(t)*v":
	# option 2: divide every element by the sum of proportions of that topic among all documents
		l = [l[i]/l2[i] for i in range(n_topics)]

	print(l)

	return l

# TODO: input only the individual lists so don't need to duplicate and then find unique

def convertTableau(dat):
	dat = dat[['topic', 'expected', 'expected_dv', 'expected_D']]
	dat.columns = ['topic', 'Topic-words', 'Doc-topics-by-d(t)*V', 'Doc-topics-by-N']
	cols = ['Topic-words', 'Doc-topics-by-d(t)*V', 'Doc-topics-by-N']
	dat = pd.melt(dat, ['topic'], cols, 'method', 'sentiment')

	dat = dat.drop_duplicates()
	return dat


def main():
	doc_topics_txt = sys.argv[1]
	documents_csv = sys.argv[2]

	existing_csv = sys.argv[3]

	tableau_csv = sys.argv[4]

	doc_topics = pd.read_csv(doc_topics_txt, sep = "\t", header = None)
	docs = pd.read_csv(documents_csv, header = 0)

	final = pd.read_csv(existing_csv, header = 0)

	new_list = expectedSen(doc_topics, docs, "d(t)*v")
	new_list_2 = expectedSen(doc_topics, docs, "n(d)")

	# merge the resulting dataset with existing_csv and re-write
	final = pd.merge(final, pd.DataFrame({'topic': range(0, len(doc_topics.columns) - 2), 
			'expected_dv': new_list, 'expected_D':new_list_2}), on = 'topic')

	final.to_csv(existing_csv, encoding='utf-8-sig', index=False)

	# convert to a CSV format for further analysis in Tableau
	final2 = convertTableau(final)
	final2.to_csv(tableau_csv, encoding = 'utf-8-sig', index = False)

main()