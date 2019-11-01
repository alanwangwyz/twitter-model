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

# Because the limits of the twitter api, each developer
#  can only use for limited number of times,so there are
#   5 accounts for the crawling of the data and 
#   just at ' para = config[N]' N is the represent each 
#   account it can switch.all the crawling will produce 
#   the to the MongoClient

import gc
import tweepy
import json
import re
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
from tweepy.streaming import StreamListener
from tweepy import Stream
import sys
import pandas as pd
from pandas.io.json import json_normalize
sys.path.append('..')
from data.parameter import config
import logging
gc.enable()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('stream-api.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def sentiment_analysis(content):
    sentiAnalyzer = SentimentIntensityAnalyzer()
    return sentiAnalyzer.polarity_scores(content)

def getKeyToken(parameter):
    auth = tweepy.OAuthHandler(parameter['consumer_key'], parameter['consumer_secret'])
    auth.set_access_token(parameter['access_token'], parameter['access_token_secret'])
    return auth

def removewebsite (tweetdata):
    try:
        text = tweetdata['extended_tweet']['full_text']
    except:
        text = tweetdata['text']
    pattern = re.compile('https://t.co/\w+')
    pat = pattern.findall(text)
    if len(pat) is 1:
        match = pat[0]
        text = text.replace(match, "")
    return text

def add_id(tweetdata):
    id=tweetdata['id']
    tweetdata['_id']=str(id)
    return tweetdata

class tweetListener(StreamListener):

    def on_data(self, data):
        tweetdata = json.loads(data)
        tweetdata = add_id(tweetdata)
        tweetReal = removewebsite(tweetdata)
        contentText1 = re.sub(r'#(\w+)\b', ' $1 ', tweetReal)
        contentText = re.sub(r'@\w+\b', '', contentText1)
        tweetid = tweetdata['id']
        print(tweetid)

        client = MongoClient('localhost', 27017)
        db = client['twitter_db']
        collection = db['twitter_collection']
        sentiment = sentiment_analysis(contentText)
        tweetdata['sentiment'] = sentiment
        # delete useless information
        del tweetdata['id']
        del tweetdata['id_str']
        del tweetdata['source']
        del tweetdata['in_reply_to_status_id']
        del tweetdata['in_reply_to_status_id_str']
        del tweetdata['in_reply_to_user_id']
        del tweetdata['in_reply_to_user_id_str']
        del tweetdata['geo']
        del tweetdata['coordinates']
        del tweetdata['place']
        del tweetdata['contributors'], tweetdata['truncated'], tweetdata['in_reply_to_screen_name']
        del tweetdata['favorited'], tweetdata['retweeted'] 
        if 'possibly_sensitive' in tweetdata:
            del tweetdata['possibly_sensitive']
        del tweetdata['filter_level']
        if 'quoted_status_id' in tweetdata:
            del tweetdata['quoted_status_id']
        if 'quoted_status_id_str' in tweetdata:
            del tweetdata['quoted_status_id_str']
        if 'retweeted_status' in tweetdata:
            del tweetdata['retweeted_status']
        if 'extended_tweet' in tweetdata:
            del tweetdata['extended_tweet']
        if 'quoted_status' in tweetdata:
            del tweetdata['quoted_status']
        if 'quoted_status_permalink' in tweetdata:
            del tweetdata['quoted_status_permalink']
        if 'is_quoted_status' in tweetdata:
            del tweetdata['is_quoted_status']
        if 'entities' in tweetdata:
            del tweetdata['entities']
        if 'user' in tweetdata:
            name = tweetdata['user']['name']
            x = {'name':name}
            tweetdata['user'] = x
            
        value = json.dumps(tweetdata, default=lambda x: x.__dict__)
        value = json.loads(value)

        try:
            collection.insert(value)
        except Exception as e:
            print(e)
        return True

    def on_status(self, status):
        print(status.text)

    def on_error(self, status):
        if status == 401:
            logger.error("Error on_error 401: Missing or incorrect authentication credentials.")
            return False

        if status == 304:
            logger.error("Error on_error 304: There was no new data to return.")
            return False

        if status == 400:
            logger.error("Error on_error 400: The request was invalid or cannot be otherwise served.")
            return False

        if status == 502:
            logger.error("Error on_error 502: Twitter is down, or being upgraded.")
            return False

        if status == 503:
            logger.error(
                "Error on_error 503: The Twitter servers are up, but overloaded with requests. Try again later.")
            return False

        if status == 504:
            logger.error(
                "Error on_error 504: The Twitter servers are up, but the request couldn’t be serviced due to some failure within the internal stack.")
            return False

        if status == 420:
            logger.error("Error on_error 420: Rate limited for making too many requests.")
            time.sleep(60)
            return False

def main():
    # This handles Twitter authetification and the connection to Twitter Streaming API
    try:

        listener = tweetListener()
        para = config[4]
        stream = Stream(getKeyToken(para), listener)
        logger.info(para['keyword'])
        # default language is English
        stream.filter(languages=["en"], track=['BTC', 'cryptocurrency', 'bitcoin'])
    except Exception as e:
        print(e)
        time.sleep(60)

main()



