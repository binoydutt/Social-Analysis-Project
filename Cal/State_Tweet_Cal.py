# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 18:43:45 2017

@author: binoy
#Priya Sanodia
#Binoy Dutt
"""



from twython import TwythonStreamer
import sys
import json
import time
from requests.exceptions import ChunkedEncodingError

state = 'Cal'

try:
    with open('tweet_stream_{}.json'.format(state), 'r') as f:
         tweets = json.load(f)
except:
    tweets = []

ctr = 0
class MyStreamer(TwythonStreamer):
    '''our own subclass of TwythonStremer'''
    # overriding
    def on_success(self, data):            
        global ctr
        ctr +=1
        #print 'tweet received # ' ,ctr
        if 'lang' in data and data['lang'] == 'en' and keyword.lower() in data['text'].lower():
            tweets.append(data)
            #print sys.getsizeof(data)            
            print 'Added tweet fulfilling filters #', len(tweets)
        if len(tweets)%100 == 0:
            time.sleep(2)
        if len(tweets) >= 10000:
            self.store_json()
            self.disconnect()

    # overriding
    def on_error(self, status_code, data):
        print status_code, data
        self.disconnect()
 
    def store_json(self):
        with open('tweet_stream_{}_{}_{}.json'.format(keyword, len(tweets),state), 'w') as f:
            json.dump(tweets, f, indent=4)


if __name__ == '__main__':

    with open('your_twitter_credentials.json', 'r') as f:
    #with open('../../../JG_Ch09_Getting_Data/04_api/gene_twitter_credentials.json', 'r') as f:
        credentials = json.load(f)

    # create your own app to get consumer key and secret
    CONSUMER_KEY = credentials['CONSUMER_KEY']
    CONSUMER_SECRET = credentials['CONSUMER_SECRET']
    ACCESS_TOKEN = credentials['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = credentials['ACCESS_TOKEN_SECRET']

    stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    lon1 = -123.8906282
    lat1 = 30.76638363
    lon2 = -117.688944
    lat2 = 34.0122346


    
  
    if len(sys.argv) > 1:
        keyword = sys.argv[1]
    else:
        keyword = 'trump'
    
    #target = [keyword.lower(), keyword.upper(),keyword.capitalize()]    
    while len(tweets)<10000:
        try:
            stream.statuses.filter(locations=[lon1,lat1,lon2,lat2])
        except ChunkedEncodingError:
            print 'Chunked Encoding Error'
        except:
            with open('tweet_stream_{}.json'.format(state), 'w') as f:
                json.dump(tweets,f, indent =4)
                print 'Keyboard Interruption or other error'
                stream.disconnect()                
                break
                

            

