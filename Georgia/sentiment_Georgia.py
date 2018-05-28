# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 15:19:09 2017

@author: binoy
#Priya Sanodia
#Binoy Dutt
"""
from textblob import TextBlob
import json
#from pprint import pprint
#import decimal #Stackoverflow http://stackoverflow.com/questions/4518641/how-to-round-off-a-floating-number
import matplotlib.pyplot as plt

state = 'Georgia'
# Reading JSON data
with open('tweet_stream_trump_10000_{}.json'.format(state), 'r') as f:
     tweets = json.load(f)
#print len(tweets)

#twt =tweets[2]
tweet_text = []
for twt in tweets:
    #b = TextBlob(twt['text'])
    #Create a list of all the tweets text
    tweet_text.append(twt['text'])

#wrtie the tweets in a text file for future use

with open('tweets_{}.json'.format(state),'w') as input:
    json.dump(tweet_text, input, indent =4)
        
sub_list = []
pol_list = []
for twt in tweet_text:
    tb = TextBlob(twt)
    #sub_list.append(round(tb.sentiment.subjectivity,2))
    #pol_list.append(round(tb.sentiment.polarity,2))
    sub_list.append(tb.sentiment.subjectivity)
    pol_list.append(tb.sentiment.polarity)    
    #print(tb_pos.sentiment)
    #pol.append(round(tb_pos.polarity,2))    
    #print('{0:.2f}'.format(tb_pos.polarity))
    #print('{0:.2f}'.format(tb_pos.subjectivity))

plt.hist(sub_list, bins=10) #, normed=1, alpha=0.75)
plt.xlabel('subjectivity score - Average is {}'.format(round(sum(sub_list)/float(len(sub_list)),2)))
plt.ylabel('Tweet count')
plt.grid(True)
plt.savefig('subjectivity_{}.pdf'.format(state))
plt.show()
plt.close()
#print len(sub_list)
#print len(pol_list)
plt.hist(pol_list, bins=20) #, normed=1, alpha=0.75)
plt.xlabel('polarity score - Average is {}'.format(round(sum(pol_list)/float(len(pol_list)),2)))
plt.ylabel('Tweet count')
plt.grid(True)
plt.savefig('polarity_{}.pdf'.format(state))
plt.show()

