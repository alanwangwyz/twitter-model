import pymongo
import pandas as pd
from datetime import datetime, timedelta, date, time as dtime
import gc
import logging
import os, pickle
import time
import numpy as np
def save_pickle(data, filepath):
    save_documents = open(filepath, 'wb')
    pickle.dump(data, save_documents)
    save_documents.close()

def load_pickle(filepath):
    documents_f = open(filepath, 'rb')
    file = pickle.load(documents_f)
    documents_f.close()
    return file

def gover_sentiment(username, sentiment):
    if username in gov_list:
        if sentiment == '+':
            return '+'
        elif sentiment == '-':
            return '-'
    return '0'

def percentage(dfnew, history):
    df1 = dfnew.sentiment.to_dict()
    df2 = {}
    for i, x in df1.items():
        if x['compound'] > 0:
            df2[i] = '+'
        elif x['compound'] == 0:
            df2[i] = ''
        else:
            df2[i] = '-'
    df3new = pd.DataFrame.from_dict(df2, orient='index')
    dfnew['New'] = df3new
    # history
    if history == 1:
        dfnew['timestamp'] = pd.to_datetime(dfnew['timestamp'], format='%Y-%m-%d')
        frequence = 'M'
        dfnew['media'] = dfnew.apply(lambda row: judge(row['fullname'], row['likes'], row['replies'], row['retweets']),
                                   axis=1)
        dfnew['GovSen'] = dfnew.apply(lambda row: gover_sentiment(row['fullname'], row['New']),
                                   axis=1)

    # recent stream
    elif history == 2:
        dfnew['timestamp'] = dfnew['timestamp_ms'].apply(lambda row: datetime.fromtimestamp(float(row) / 1000.0))
        frequence = 'D'
        name = dfnew['user'].to_dict()
        n = {}
        for i, x in name.items():
            n[i] = x['name']
        dfnew['name'] = pd.DataFrame.from_dict(n, orient='index')
        dfnew['media'] = dfnew.apply(
            lambda row: judge(row['name'], row['favorite_count'], row['reply_count'], row['retweet_count']), axis=1)
        dfnew['GovSen'] = dfnew.apply(lambda row: gover_sentiment(row['name'], row['New']),axis=1)

    # archive
    else:
        dfnew['timestamp'] = pd.to_datetime(dfnew['created_at'], infer_datetime_format=True)
        dfnew['timestamp'] = dfnew['timestamp'].dt.date
        dfnew['timestamp'] = pd.to_datetime(dfnew['timestamp'], format='%Y-%m-%d')
        frequence = 'M'
        name = dfnew['user'].to_dict()
        n = {}
        for i, x in name.items():
            n[i] = x['name']
        dfnew['name'] = pd.DataFrame.from_dict(n, orient='index')
        dfnew['media'] = dfnew.apply(
            lambda row: judge(row['name'], row['favorite_count'], row['reply_count'], row['retweet_count']), axis=1)
        dfnew['GovSen'] = dfnew.apply(lambda row: gover_sentiment(row['name'], row['New']), axis=1)


    neu = dfnew.groupby([pd.Grouper(key='timestamp', freq=frequence, label='left')])['New'].apply(
        lambda x: (x == '').sum()).reset_index(name='neu')
    pos = dfnew.groupby([pd.Grouper(key='timestamp', freq=frequence, label='left')])['New'].apply(
        lambda x: (x == '+').sum()).reset_index(name='pos')
    neg = dfnew.groupby([pd.Grouper(key='timestamp', freq=frequence, label='left')])['New'].apply(
        lambda x: (x == '-').sum()).reset_index(name='neg')
    total = dfnew.groupby([pd.Grouper(key='timestamp', freq=frequence, label='left')]).size().reset_index(name='total')
    medium_influence = dfnew.groupby([pd.Grouper(key='timestamp', freq=frequence, label='left')])['media'].apply(
        lambda x: (x == '1').sum()).reset_index(name='MInfluence')
    Govpos = dfnew.groupby([pd.Grouper(key='timestamp', freq=frequence, label='left')])['GovSen'].apply(
        lambda x: (x == '+').sum()).reset_index(name='Govpos')
    Govneg = dfnew.groupby([pd.Grouper(key='timestamp', freq=frequence, label='left')])['GovSen'].apply(
        lambda x: (x == '-').sum()).reset_index(name='Govneg')
    Govtotal = dfnew.groupby([pd.Grouper(key='timestamp', freq=frequence, label='left')])['GovSen'].apply(
        lambda x: (x != '0').sum()).reset_index(name='Govtotal')
    dfnew = pd.merge(neu, pos)
    dfnew = pd.merge(dfnew, neg)
    dfnew = pd.merge(dfnew, total)
    dfnew = pd.merge(dfnew, medium_influence)
    dfnew = pd.merge(dfnew, Govpos)
    dfnew = pd.merge(dfnew, Govneg)
    dfnew = pd.merge(dfnew, Govtotal)
    dfnew['neup'] = dfnew['neu'] / dfnew['total']
    dfnew['posp'] = dfnew['pos'] / dfnew['total']
    dfnew['negp'] = dfnew['neg'] / dfnew['total']
    dfnew['Govposp'] = (dfnew['Govpos']/dfnew['Govtotal']).replace(np.nan, 0)
    dfnew['Govnegp'] = (dfnew['Govneg']/dfnew['Govtotal']).replace(np.nan, 0)
    dfnew = dfnew.dropna()
    dfnew = dfnew.reset_index()
    dfnew = dfnew.drop(columns=['index'])
    return dfnew

def difference(history):
    history['pos_change'] = history['posp'].diff()
    history['neg_change'] = history['negp'].diff()
    history['Govpos_change'] = history['Govposp'].diff()
    history['Govneg_change'] = history['Govnegp'].diff()
    history['GovIspos'] = history['Govpos_change'].apply(lambda x: tag(x))
    history['GovIsneg'] = history['Govneg_change'].apply(lambda x: tag(x))
    history['Ispos'] = history['pos_change'].apply(lambda x: tag(x))
    history['Isneg'] = history['neg_change'].apply(lambda x: tag(x))
    # history['timestamp'] = history.index
    # history.index = history['timestamp']
    # history = history.set_index('timestamp').resample('D').ffill()
    return history
def tag(context):
    if context is None:
        return 0
    elif context > 0:
        return 1
    return 0



gov_list = ['KUCOIN', 'Bitcoin', 'The Onion', 'Coinbase', 'CoinPulse Exchange', 'The Spectator Index', 'Netkoin',
                'Substratum', 'Bitcoin Turbo Koin', 'Crypto Airdrops', 'Bethereum', 'PO8', 'CCN.com', 'The FREE COIN',
                'CryptoTown', 'CryptoPuppies', 'OPEN Platform', 'Bitstamp', 'Phore Blockchain', 'CoinDesk',
                'cotrader.com', 'Altcoins Talks', 'Crypto Rand', 'Cointelegraph', 'CryptoKing', 'Crypto Boss',
                'INSCoin', 'eBTCS', 'CNBC', 'The Economist', 'ABCC Exchange', 'BitPlay™', 'WuxinBTC-NEWS',
                'InvestInBlockchain.com', 'Bitcoin Modern Vision', 'ABCC Exchange', 'Storm Play', 'Bitcoin Plus Cash',
                'Altcoin.io Exchange', 'CoinBene Global', 'Cryptelo', 'Coincheck(コインチェック)', 'MarketWatch',
                'CryptoCret | Bitcoin and Cryptocurrency News', 'NeedsCoin', 'Poloniex Exchange', 'Crypto Currency',
                'Cash App']

def judge(fullname, likes, replies, retweets):
    if fullname in gov_list:
        return '2'
    elif likes>9 and replies>3 and retweets>8:
        return '1'
    else:
        return '0'
try:
    gc.enable()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('sentiment.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info('============================================')
    start_date = datetime.combine(date.today() - timedelta(days=1), dtime(14, 0))
    end_date = datetime.combine(date.today(), dtime(14, 0))
    logger.info("Start date: {}; end date: {}.".format((start_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                                                       end_date.strftime('%Y-%m-%d')))
    client = pymongo.MongoClient('localhost', 27017)
    db = client['twitter_db']

    file_extraction_start = time.time()
    history=load_pickle(os.path.join('history.p'))
    # collection = db['twitter_collection_2016-2018']
    # history = pd.DataFrame(list(collection.find()))
    # history = percentage(history, 1)
    # collection = db['twitter_collection_5_8_17']
    # archive = pd.DataFrame(list(collection.find()))
    # archive = percentage(archive, 0)
    # collection = db['twitter_collection_13_10']
    # archiveold = pd.DataFrame(list(collection.find()))
    # archiveold = percentage(archiveold, 0)
    collection = db['twitter_collection_new']
    recent = pd.DataFrame(list(collection.find()))
    
    recent = percentage(recent, 2)
    print(recent)
    history = pd.concat([history, recent], sort=True)
    
    
    history.index = history['timestamp']
    # save_pickle(history, os.path.join('historynow.p'))
    
    history.sort_index(inplace=True)
    print(history)
    # datetime_object = datetime.strptime('Sep 13 2011', '%b %d %Y')
    # history.loc[0] = [0, 0, 5, 1, 5, 0, 455, 0.080000, 3450, 0.630000, 1640, 0.298182, datetime_object, 5500]


    # print('second')
    # print(history)
    # history.sort_index(inplace=True)
    # history.index = history['timestamp']
    # history.sort_index(inplace=True)
    
    # today = pd.DataFrame()
    history=difference(history)
    # if history['timestamp'].iloc[len(history)-1].date()==datetime.now().date():
    #     history.drop(history.tail(1).index, inplace = True)
    # print(history)
	
    datetime1 = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
    new = history.iloc[len(history) - 1]
    new = new.to_dict()

    history = history.append(pd.DataFrame(new, index=[datetime1]))
    history['timestamp'] = history.index
    history.index = history['timestamp']
    history = history.drop_duplicates(subset='timestamp', keep="first")
    # print(history)
    
    
    history = history.resample('D').ffill()

    history['timestamp'] = history.index
    # print(history)

    old = load_pickle(os.path.join("../data/stock_price.p"))
    history['date'] = history.index
    old['date'] = old.index
    history = pd.merge(old, history, how='right')
    
    history.index = history['timestamp']
    # # save_pickle(history, os.path.join('final.p'))
    history = history.iloc[-30:]
    print(history)
    history.to_json(r'../JSON/SentimentChange.json', orient='records', date_format='iso', date_unit='s')
    # today.to_json(r'../JSON/SentimentChangeToday.json', orient='records', date_format='iso', date_unit='s')
    
    gc.collect()
except Exception as e:
    print(e)



