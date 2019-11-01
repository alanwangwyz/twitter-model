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

# our attempt to crawl the data.

import gc
import logging
import quandl
from datetime import datetime, timedelta, date, time as dtime
import os, pickle
import pymongo

gc.enable()
def save_pickle(data, filepath):
    save_documents = open(filepath, 'wb')
    pickle.dump(data, save_documents)
    save_documents.close()
try:
    # from quandl collect stock price information #
    quandl.ApiConfig.api_key = "nJNHyQjJHj7U8ygzTUzW"
    df = quandl.get("BCHARTS/BITSTAMPUSD")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler('stock price collection.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info('============================================')
    start_date = datetime.combine(date.today() - timedelta(days=1), dtime(14, 0))
    end_date = datetime.combine(date.today(), dtime(14, 0))
    logger.info("Start date: {}; end date: {}.".format((start_date + timedelta(days=1)).strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    #save price pickle
    save_pickle(df, os.path.join('stock_price.p'))
    # Save into mongo as well
    client = pymongo.MongoClient('localhost', 27017)
    db = client['twitter_backup']
    collection = db['PriceBackup']
    collection.insert_many(df.to_dict('records'))
    logger.info("Stock info get updated until: {} and successfully saved.".format(df.index[-1]))
    del df
    gc.collect()
except Exception as e:
    logger.error(e)






