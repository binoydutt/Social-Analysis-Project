# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 01:53:59 2017

@author: binoy
#Priya Sanodia
#Binoy Dutt
"""
from __future__ import division, print_function
import json
import numpy as np  # a conventional alias
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import decomposition


from gensim import corpora, models, similarities, matutils
import logging

state ='NY'
with open('tweet_filtered_{}.json'.format(state), 'r') as f:
    tweets = json.load(f)


vectorizer = TfidfVectorizer(stop_words='english', min_df=2)
doc_term_matrix = vectorizer.fit_transform(tweets)
print (doc_term_matrix.shape)
vocab = vectorizer.get_feature_names() # list of unique vocab, we will use this later
#print len(vocab), '# of unique words'
#print vocab[-10:] # last ten keywords
#print vocab[:10] # first ten keywords

num_topics = 5

clf = decomposition.NMF(n_components=num_topics, random_state=1)
doc_topic = clf.fit_transform(doc_term_matrix)
print (type(doc_topic), doc_topic.shape)
print ( num_topics, clf.reconstruction_err_)

vocab = vectorizer.get_feature_names()
#print vocab

topic_words = []
num_top_words = 6

for topic in clf.components_:
    #print topic.shape, topic[:5]
    word_idx = np.argsort(topic)[::-1][0:num_top_words] # get indexes with highest weights
#    print 'top indexes', word_idx
    topic_words.append([vocab[i] for i in word_idx])


topic_list =[]    
txt =''
for words in topic_words:
    txt =''    
    for word in words:    
        txt += ' {}'.format(word)
    topic_list.append(txt)

with open('topic_list_NFM_{}_{}.json'.format(state,num_topics),'w') as f:
    json.dump(topic_list,f,indent=4)
    
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

tweet = []
for twt in tweets:
    tweet.append(twt.split())
    

dic = corpora.Dictionary(tweet)
print(dic)

corpus = [dic.doc2bow(text) for text in tweet]
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

NUM_TOPICS = 5
model = models.ldamodel.LdaModel(corpus_tfidf, 
                                 num_topics=NUM_TOPICS, 
                                 id2word=dic, 
                                 update_every=1, 
                                 passes=100)

topics_found = model.print_topics(num_topics = 5, num_words = 6)
topics = []
for t in topics_found:
    #print(t[1].split('+'), type(t[1]))
    topics.append(t[1].split('+'))
'''
topics = []
with open('topic_list_LDA_Draft.json','r') as g:
    topics = json.load(g)
'''
topic_LDA = []
for lst in topics:
    txt = ''
    for words in lst:
        txt += ' {}'.format(words.split('"')[1])
    topic_LDA.append(txt)
    
with open('topic_list_LDA_{}_{}.json'.format(state,num_topics),'w') as g:
    json.dump(topic_LDA,g,indent=4)
    
