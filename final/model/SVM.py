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

# This part we just call the function 'from sklearn.svm import SVR'
# to get  Support victor machine apply to the gov sentiment analysis
#  and to produce the SVMTwitter.json as the result.
import gc
import plotly
import matplotlib.dates as mdates
from sklearn.svm import SVR
import threading
import numpy as np
import json
import pandas as pd
from os import sys
from fastai.structured import *
sys.path.append('..')
from model import useful_function

gc.enable()


class SVMmodel(threading.Thread):
    def __init__(self, data, logging):
        threading.Thread.__init__(self)
        self.data = data
        self.logging = logging
        self.valid = 0.2
        self.length = 0
        self.rmse = {}
        self.info = {}


    def run(self):
        total = {}
        data = self.data
        data['Date'] = data['timestamp'].map(mdates.date2num)
        new_data = pd.DataFrame(index=range(0, len(data)), columns=['Date', 'Close'])
        for i in range(0, len(data)):
            new_data['Date'][i] = data['Date'][i]
            new_data['Close'][i] = data['Close'][i]
        # transform data according to Fastai
        add_datepart(new_data, 'Date')
        new_data.drop('Elapsed', axis=1, inplace=True)
        new_data['mon_fri'] = 0
        def check(date):
            if date == 0 or date == 4:
                return 1
            return 0
        new_data['mon_fri'] = new_data['Dayofweek'].apply(lambda row: check(row))
        new_data.index = data['timestamp']
        data1 = new_data.copy()
        new_data['neg'] = data['Isneg']
        new_data['pos'] = data['Ispos']
        data2 = new_data.copy()
        new_data['Gneg'] = data['GovIsneg']
        new_data['Gpos'] = data['GovIspos']
        self.length = int(len(new_data) * (1 - self.valid))
        train_ = new_data
        valid = new_data[self.length:]

        x_train = train_.drop('Close', axis=1)
        y_train = train_['Close']
        x_valid = valid.drop('Close', axis=1)
        y_valid = valid['Close']


        train1 = data1
        valid1 = data1[self.length:]
        x_train1 = train1.drop('Close', axis=1)
        y_train1 = train1['Close']
        x_valid1 = valid1.drop('Close', axis=1)
        y_valid1 = valid1['Close']

        train2 = data2
        valid2 = data2[self.length:]
        x_train2 = train2.drop('Close', axis=1)
        y_train2 = train2['Close']
        x_valid2 = valid2.drop('Close', axis=1)
        y_valid2 = valid2['Close']

        # build model
        svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
        svr_rbf.fit(x_train, y_train)
        preds = svr_rbf.predict(x_valid)
        # evaluation
        rms1 = np.sqrt(np.mean(np.power((np.array(y_valid) - np.array(preds)), 2)))
        self.logging.info('SVM')
        self.logging.info('RMSE value on validation set with +/- and Government: {}.'.format(rms1))
        print('RMSE value on validation set with +/- and Government SVM:')
        print(rms1)
        MAPE = np.mean(np.abs(np.array(y_valid) - np.array(preds) / np.array(y_valid)))
        self.logging.info('MAPE value on validation set with +/- and Government: {}.'.format(MAPE))
        print('MAPE value on validation set with +/- and Government:')
        print(MAPE)
        t = []
        t.append(rms1)
        t.append(MAPE)
        total['GT'] = t
        valid['Predict_Twitter'] = preds
        self.rmse[rms1] = x_train, y_train, svr_rbf, new_data

        # build model
        svr_rbf1 = SVR(kernel='rbf', C=1e3, gamma=0.1)
        svr_rbf1.fit(x_train1, y_train1)
        preds1 = svr_rbf1.predict(x_valid1)
        rms2 = np.sqrt(np.mean(np.power((np.array(y_valid1) - np.array(preds1)), 2)))
        # evaluation
        self.logging.info('RMSE value on validation set : {}.'.format(rms2))
        print('RMSE value on validation set with SVM:')
        print(rms2)
        MAPE1 = np.mean(np.abs(np.array(y_valid1) - np.array(preds1) / np.array(y_valid1)))
        self.logging.info('MAPE value on validation set: {}.'.format(MAPE1))
        print('MAPE value on validation set:')
        print(MAPE1)
        valid1['Predict_Twitter'] = preds1
        self.rmse[rms2] = x_train1, y_train1, svr_rbf1, data1
        t1 = []
        t1.append(rms2)
        t1.append(MAPE1)
        total['N'] = t1

        # build model
        svr_rbf2 = SVR(kernel='rbf', C=1e3, gamma=0.1)
        svr_rbf2.fit(x_train2, y_train2)
        preds2 = svr_rbf2.predict(x_valid2)
        # evaluation
        rms3 = np.sqrt(np.mean(np.power((np.array(y_valid2) - np.array(preds2)), 2)))
        self.logging.info('RMSE value on validation set with +/- : {}.'.format(rms3))
        print('RMSE value on validation set with SVM:')
        print(rms3)
        MAPE2 = np.mean(np.abs(np.array(y_valid2) - np.array(preds2) / np.array(y_valid2)))
        self.logging.info('MAPE value on validation set with +/- : {}.'.format(MAPE2))
        print('MAPE value on validation set:')
        print(MAPE2)
        valid2['Predict_Twitter'] = preds2
        t2 = []
        t2.append(rms3)
        t2.append(MAPE2)
        total['T'] = t2
        self.rmse[rms3] = x_train2, y_train2, svr_rbf2, data2

        # make prediction with minimum RMSE
        index = min(self.rmse.keys())
        newx_train, newy_train, new_model, newd = self.rmse.get(index)
        stdev = np.sqrt(sum((new_model.predict(newx_train) - newy_train) ** 2) / (len(newy_train) - 2))
        predict = useful_function.FunctionalTools.predict(365, new_model, stdev, newd, 'SVM')
        fig = useful_function.FunctionalTools.plot_intervals(predict)
        # produce graph
        fig1 = useful_function.FunctionalTools.evaluate('SVM with Twitter and Government\n RMSE: \t', rms1, train_,
                                        valid, valid, index, fig)
        with open('../JSON/SVMTwitterGovernment.json', 'w') as outfile:
            json.dump(fig1, outfile, cls=plotly.utils.PlotlyJSONEncoder)


        fig2 = useful_function.FunctionalTools.evaluate('SVM \n RMSE: \t', rms2, train_, valid, valid1, index, fig)
        with open('../JSON/SVM.json', 'w') as outfile:
            json.dump(fig2, outfile, cls=plotly.utils.PlotlyJSONEncoder)


        fig3 = useful_function.FunctionalTools.evaluate('SVM with Twitter \n RMSE: \t', rms3, train_, valid,
                                        valid2, index, fig)
        with open('../JSON/SVMTwitter.json', 'w') as outfile:
            json.dump(fig3, outfile, cls=plotly.utils.PlotlyJSONEncoder)
        self.info['SVM'] = total
        self.logging.info('SVM Models have been saved!')
        gc.collect()

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self.info
