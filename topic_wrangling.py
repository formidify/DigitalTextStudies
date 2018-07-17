import sys

import pandas
import re
import numpy as np

import sklearn
from sklearn import manifold

'''
This Python file takes a CSV with columns 'topic', 'word', 'count', and calculate the proportion of each word within a topic, 
merge it with the SentiWords lexicon dictionary, and calculates the distances between any 2 topics, and uses Python sklearn
MDS toolkit to generate the coordinates of eacu topic in an Euclidean space. 

input: a CSV file of topics of a dataset and the CSV file you want the result to be in
return: a CSV file with columns: 'topic', 'word', 'count', 'prop', 'score', 'x', 'y'
'''

def main():
    txt = sys.argv[1]
    csv_final = sys.argv[2]

    # clean the topic model text into a data frame first
    file = open(txt)
    df = pandas.DataFrame(columns = ['topic', 'word', 'count'])
    track = 0

    for line in file:
        l = line.split()
        word = l[1]
        for i in range(len(l)-2):
            cur = [int(i) for i in l[i+2].split(":")]
            topic = cur[0]
            count = cur[1]
            df.loc[track] = [topic, word, count]
            track += 1


    lexicon = pandas.read_csv("SentiWords_cleaned.csv", encoding='utf-8-sig')

    num_topics = max(df['topic'])+1

    dfs = []
    for i in range(num_topics):
        df_i = df.loc[df['topic'] == i].copy()
        s = df_i['count'].sum()
        df_i['prop'] = df_i['count'].apply(lambda g: g/s)
        dfs.append(df_i)

    df = pandas.concat(dfs)
    
    # join two datasets
    df = pandas.merge(df, lexicon, on='word', how='left')
    
    # filter out null values (thus all the words in a single topic do not add up to 1)
    df = df[df['score'].notnull()]
    
    df = reset(df)

    ## Calculating distance matrices (2 options)

    mat = [[0 for _ in range(num_topics)] for _ in range(num_topics)]
    all_words = df['word'].unique()

    # a) calculate coordinates by creating a distance matrix from euclidean distance
    '''
    topics_list = [i for i in range(num_topics)] # set as static

    for i in range(len(all_words)):
        word = all_words[i]
        df_word = df.loc[df['word'] == word].copy()
        num_words = df_word.shape[0]
        
        df_word = reset(df_word)

        prop_list = [0 for i in range(num_topics)]

        # fill in the proportion of a word in all the topics
        for j in range(num_words):
            prop_list[df_word.loc[j, 'topic']] = df_word.loc[j, 'prop']


        for m in range(num_topics):
            for n in range(m+1, num_topics):
                dist = (prop_list[m]- prop_list[n]) ** 2

                mat[m][n] = mat[m][n] + dist
                mat[n][m] = mat[n][m] + dist
    '''

    # Takes 2 vectors a, b and returns the cosine similarity between the two. Codes created by Mason Gallo (see
    # https://masongallo.github.io/machine/learning,/python/2016/07/29/cosine-similarity.html for more details).

    def cos_sim(a, b):
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        return dot_product / (norm_a * norm_b)

    # b) instead of calculating euclidean distance between vectors, use cosine similarity instead

    vectors = [[0 for _ in range(all_words.shape[0])] for _ in range(num_topics)]

    for i in range(len(all_words)):
        word = all_words[i]
        df_word = df.loc[df['word'] == word].copy()
        num_words = df_word.shape[0]

        df_word = reset(df_word)

        for j in range(num_words):
            vectors[df_word.loc[j, 'topic']][i] = df_word.loc[j, 'prop']

    for m in range(num_topics):
        for n in range(m+1, num_topics):
            dist = cos_sim(vectors[m], vectors[n])
            mat[m][n] = dist
            mat[n][m] = dist

    # print(mat)
    constant = 20000 # set this as how much you want the distance matrix to be multipled by
    mat = [[constant * mat[i][j] for j in range(num_topics)] for i in range(num_topics)]

    # use the distance/dissimilarity matrix and MDS to calculate coordinates for each topic
    mod = manifold.MDS(max_iter = 3000, dissimilarity = 'precomputed')
    result = mod.fit(mat)
    print("The stress level is", result.stress_)
    coords = result.embedding_
    print(coords) # testing

    # add the coordinates to th CSV by joining two CSVs
    x_coords = [coords[i][0] for i in range(num_topics)]
    y_coords = [coords[i][1] for i in range(num_topics)]
    coords_df = pandas.DataFrame({'topic': range(0, num_topics), 'x': x_coords, 'y': y_coords})

    df = pandas.merge(df, coords_df, on='topic')

    ## group by the data frame and calculate the expected sentiment value for each topic
    df['helper'] = df['prop']*df['score']
    help_dat = pandas.DataFrame({'topic': range(0, num_topics), 'expected': df.groupby(['topic'])['helper'].sum()})

    '''
    help_dat = findSentiment(doc_topics, documents) # the other option to calculate expected sentiments
    '''
    print(help_dat['expected'])

    # scale the expected values so that they work on the color scales in D3 better
    maxVal = abs(help_dat['expected']).max()
    normal_const = 1/abs(maxVal)
    help_dat['expected_scaled'] = help_dat.loc[:, 'expected'] * (1) * normal_const # 1/-1 is when the diverging scale needs to be flipped

    df.drop('helper', axis = 1)
    df = pandas.merge(df, help_dat, on = 'topic')

    # only keep words with count > 1
    df = df[df['count'] > 1]
    
    df = reset(df)

    # convert to csv
    df.to_csv(csv_final, encoding='utf-8-sig', index=False)

# resets index and delete old index column
def reset(df):
    df = df.reset_index()
    df = df.drop('index', 1)
    return df

main()
