# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 19:58:52 2017

@author: binoy
#Priya Sanodia
#Binoy Dutt
"""
from __future__ import unicode_literals
from wordcloud import WordCloud
import unicodedata #http://stackoverflow.com/questions/1207457/convert-a-unicode-string-to-a-string-in-python-containing-extra-symbols
import json
import nltk
import string
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

#from gensim.summarization import keywords
#from textblob import TextBlob


import matplotlib.pyplot as plt

state = 'Cal'
#n6download_shell()
with open('tweets_{}.json'.format(state), 'r') as f:
     tweets = json.load(f)

ps = PorterStemmer()
#wnl = WordNetLemmatizer()
stem_tweet = []     
stopwords = nltk.corpus.stopwords.words('english')



p = string.punctuation
d = string.digits
table_p = string.maketrans(p, len(p) * " ")
table_d = string.maketrans(d, len(d) * " ")

wordcloud_tweet = []
txt1=''
txt2 = ''
for twt in tweets:
    tx = unicodedata.normalize('NFKD', twt).encode('ascii','ignore')
    txt1 = tx.translate(table_p)
    txt2 = txt1.translate(table_d)
    wordcloud_tweet.append(txt2)

#Tweets is a list of tweets hence a loop going over each tweet and over each word
#Each word is then stripped of \n and are stemmed
ignore_words = ['RT', 'rt','http', 'https', 'trump','donald', 'realdonaldtrump', 'thi', 'amp','hi','whi','co','ha','potus','potu','wa','president']
accept_words = ['trumpcare', 'obamacare','notmypresident']
for twt in wordcloud_tweet:
    txt=''
    for word in twt.split():
        word_txt = word.lower().strip('\n')        
        if word_txt in ignore_words or len(word_txt) == 1:
            continue
        if word_txt in accept_words:
            txt += ' {}'.format(word_txt)
        else:
            stem_word = ps.stem(word_txt)            
            txt += ' {}'.format(stem_word)
    stem_tweet.append(txt)
    



stop_tweets =[]

for twt in stem_tweet:
    txt =''
    for word in twt.split():
        #removing stop words, single length words and the word RT
        if word in stopwords or word in ignore_words:
            continue
        txt += ' {}'.format(word.lower())
    stop_tweets.append(txt)



#print stop_tweets
txt =''
for twt in stop_tweets:
    for words in twt.split():
        txt += ' {}'.format(words)

        
wordcloud = WordCloud().generate(txt)

# Display the generated image:
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('WordCloud_{}.pdf'.format(state))
#plt.show()

#print keywords(txt)

with open('tweet_filtered_{}.json'.format(state), 'w') as f:
    json.dump(stop_tweets, f, indent = 4)

