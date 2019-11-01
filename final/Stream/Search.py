#University of Melbourne
#School of computing and information systems
#Master of Information Technology
#Semester 2, 2019
#2019-SM2-COMP90055: Computing Project
#Software Development Project
#Cryptocurrency Analytics Based on Machine Learning
#Supervisor: Prof. Richard Sinnott
#Team member :Tzu-Tung HSIEH (818625)
#             Yizhou WANG (669026)
#             Yunqiang PU (909662)

# archive history search 

from TwitterAPI import TwitterAPI
import json
from pymongo import MongoClient
import re
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

client = MongoClient('localhost', 27017)
db = client['twitter_db']
collection = db['twitter_collection_14']

def sentiment_analysis(content):
    sentiAnalyzer = SentimentIntensityAnalyzer()
    return sentiAnalyzer.polarity_scores(content)


def remove_url(text):
    result = re.sub(r"http\S+", "", text)
    return result

for i in range(50):
    SEARCH_TERM = 'BTC'
    
    consumer_key = 'n6LyNaP5EboggbbX54LI8V6NC'
    consumer_secret = 'f5ZoX5k1hISAbW1LKjgQoemjP9RZ08TSpHexeuyiY2imsrojbN'
    access_token = '863425363-t1toS1SzXZO3Y4OrOIYZZhN1adhXX8O2jzhDzOtj'
    access_token_secret = 'PrL1I16jiVwqvO7HjbpdtADKAcGNu46Km4JT73KLxm3lI'
    api = TwitterAPI(consumer_key,
             consumer_secret,
             access_token,
             access_token_secret)
    
    PRODUCT = 'fullarchive'
    LABEL = 'project'
    r = api.request('tweets/search/%s/:%s' % (PRODUCT, LABEL),
            {'query': SEARCH_TERM,
            'fromDate':'201410010000',
            'toDate':'201410012359',
             "maxResults":100
            })
    ds = []
    for item in r:      # your loop
        ds += [item]
    new = pd.DataFrame(ds)
    new['text'] = new['text'].apply(lambda row: remove_url(str(row)))
    new['sentiment'] = new['text'].apply(lambda row: sentiment_analysis(str(row)))
    collection.insert_many(new.to_dict(orient = 'records'))
    print(str(i)+"finish!")