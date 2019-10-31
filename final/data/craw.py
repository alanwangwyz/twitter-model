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
    save_pickle(df, os.path.join('stock_price.p'))
    client = pymongo.MongoClient('localhost', 27017)
    db = client['twitter_backup']
    collection = db['PriceBackup']
    collection.insert_many(df.to_dict('records'))
    logger.info("Stock info get updated until: {} and successfully saved.".format(df.index[-1]))
    del df
    gc.collect()
except Exception as e:
    logger.error(e)






