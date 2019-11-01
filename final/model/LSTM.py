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

# This part we just call the function 'from keras.
# layers import Dense, LSTM'to get Long Short-Term
#  Memory model applyed to the gov sentiment analysis
#   and to produce the '../JSON/LSTM' + str(90) + '.
#   json' as the result.

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import pandas as pd
import numpy as np
import gc
import plotly
import plotly.graph_objs as go
import json
import threading
gc.enable()


class LSTMmodel(threading.Thread):
    def __init__(self, data, logging):
        threading.Thread.__init__(self)
        self.data = data
        self.logging = logging
        self.valid = 0.2
        self.length = 0
        self.info = {}


    def run(self):
        self.logging.info('LSTM')
        total = {}
        data = self.data
        data['timestamp'] = pd.to_datetime(data.index, format='%Y-%m-%d')
        data.index = data['timestamp']
        data['Date'] = data.index
        t=[]

        data = data.sort_index(ascending=True, axis=0)
        new_data = pd.DataFrame(index=range(0, len(data)), columns=['Date', 'Close'])
        for n in range(0, len(data)):
            new_data['Date'][n] = data['Date'][n]
            new_data['Close'][n] = data['Close'][n]

        new_data.index = new_data.Date
        new_data.drop('Date', axis=1, inplace=True)
        dataset = new_data.values
        self.length = int(len(dataset) * (1 - self.valid))
        train = dataset
        valid = dataset[self.length:, :]

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)
        x_train, y_train = [], []
        for j in range(30, len(train)):
            x_train.append(scaled_data[j - 30:j, 0])
            y_train.append(scaled_data[j, 0])
        x_train, y_train = np.array(x_train), np.array(y_train)

        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # create and fit the LSTM network
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(units=50))
        model.add(Dense(1))

        model.compile(loss='mean_squared_error', optimizer='adam')
        model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

        inputs = new_data[len(new_data) - len(valid) - 30:].values
        inputs = inputs.reshape(-1, 1)
        inputs = scaler.transform(inputs)

        X_test = []
        for x in range(30, inputs.shape[0]):
            X_test.append(inputs[x - 30:x, 0])
        X_test = np.array(X_test)

        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        closing_price = model.predict(X_test)
        closing_price = scaler.inverse_transform(closing_price)
        rms1 = np.sqrt(np.mean(np.power((valid - closing_price), 2)))

        self.logging.info('RMSE value on validation set:' + 'Lag = ' + str(30) + ':{}'.format(rms1))
        print('\n RMSE value on validation set:' + 'Lag = ' + str(30))
        print(rms1)
        MAPE1 = np.mean(
            np.abs(np.array(valid) - np.array(closing_price) / np.array(closing_price)))
        train = new_data
        valid = new_data[self.length:]
        valid['Predict_Twitter'] = closing_price
        t.append(rms1)
        t.append(MAPE1)
        total['30'] = t

        # produce graph
        fig6 = go.Figure()
        fig6.update_layout(width=1000,height=700,title='LSTM \n Using Lag' + str(30) + ' RMSE ' + "{0:.2f}".format(rms1),
                           yaxis=go.layout.YAxis(
                               title=go.layout.yaxis.Title(
                                   text="Price",
                                   font=dict(
                                       family="Courier New, monospace",
                                       size=18,
                                       color="#7f7f7f"
                                   )
                               )
                           ))
        btc_train = go.Scatter(x=train.index, y=train['Close'], name='History')
        btc_test = go.Scatter(x=valid.index, y=valid['Close'], name='Actual')
        btc_test_ = go.Scatter(x=valid.index, y=valid['Predict_Twitter'], name='Predictions')
        fig6.add_trace(btc_train)
        fig6.add_trace(btc_test)
        fig6.add_trace(btc_test_)

        with open('../JSON/LSTM' + str(30) + '.json', 'w') as outfile:
            json.dump(fig6, outfile, cls=plotly.utils.PlotlyJSONEncoder)


        data = self.data
        data['timestamp'] = pd.to_datetime(data.index, format='%Y-%m-%d')
        data.index = data['timestamp']
        data['Date'] = data.index

        data = data.sort_index(ascending=True, axis=0)
        new_data = pd.DataFrame(index=range(0, len(data)), columns=['Date', 'Close'])
        for n in range(0, len(data)):
            new_data['Date'][n] = data['Date'][n]
            new_data['Close'][n] = data['Close'][n]

        new_data.index = new_data.Date
        new_data.drop('Date', axis=1, inplace=True)

        dataset = new_data.values
        self.length = int(len(dataset) * (1 - self.valid))
        train1 = dataset
        valid1 = dataset[self.length:, :]

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)
        x_train1, y_train1 = [], []
        for j in range(60, len(train1)):
            x_train1.append(scaled_data[j - 60:j, 0])
            y_train1.append(scaled_data[j, 0])
        x_train1, y_train1 = np.array(x_train1), np.array(y_train1)

        x_train1 = np.reshape(x_train1, (x_train1.shape[0], x_train1.shape[1], 1))

        # create and fit the LSTM network
        model1 = Sequential()
        model1.add(LSTM(units=50, return_sequences=True, input_shape=(x_train1.shape[1], 1)))
        model1.add(LSTM(units=50))
        model1.add(Dense(1))

        model1.compile(loss='mean_squared_error', optimizer='adam')
        model1.fit(x_train1, y_train1, epochs=1, batch_size=1, verbose=2)

        inputs = new_data[len(new_data) - len(valid1) - 60:].values
        inputs = inputs.reshape(-1, 1)
        inputs = scaler.transform(inputs)

        X_test2 = []
        for x in range(60, inputs.shape[0]):
            X_test2.append(inputs[x - 60:x, 0])
        X_test2 = np.array(X_test2)

        X_test2 = np.reshape(X_test2, (X_test2.shape[0], X_test2.shape[1], 1))
        closing_price2 = model1.predict(X_test2)
        closing_price2 = scaler.inverse_transform(closing_price2)
        rms2 = np.sqrt(np.mean(np.power((valid1 - closing_price2), 2)))

        self.logging.info('RMSE value on validation set:' + 'Lag = ' + str(60) + ':{}'.format(rms2))
        print('\n RMSE value on validation set:' + 'Lag = ' + str(60))
        print(rms2)
        MAPE2 = np.mean(
            np.abs(np.array(valid1) - np.array(closing_price2) / np.array(closing_price2)))
        train1 = new_data
        valid1 = new_data[self.length:]
        valid1['Predict_Twitter'] = closing_price2
        t1=[]
        t1.append(rms2)
        t1.append(MAPE2)
        total['60'] = t1

        # produce graph
        fig7 = go.Figure()
        fig7.update_layout(width=1000,height=700,title='LSTM \n Using Lag' + str(60) + ' RMSE ' + "{0:.2f}".format(rms2),
                           yaxis=go.layout.YAxis(
                               title=go.layout.yaxis.Title(
                                   text="Price",
                                   font=dict(
                                       family="Courier New, monospace",
                                       size=18,
                                       color="#7f7f7f"
                                   )
                               )
                           ))
        btc_train = go.Scatter(x=train1.index, y=train1['Close'], name='History')
        btc_test = go.Scatter(x=valid.index, y=valid['Close'], name='Actual')
        btc_test_ = go.Scatter(x=valid1.index, y=valid1['Predict_Twitter'], name='Predictions')
        fig7.add_trace(btc_train)
        fig7.add_trace(btc_test)
        fig7.add_trace(btc_test_)

        with open('../JSON/LSTM' + str(60) + '.json', 'w') as outfile:
            json.dump(fig7, outfile, cls=plotly.utils.PlotlyJSONEncoder)


        data = self.data
        data['timestamp'] = pd.to_datetime(data.index, format='%Y-%m-%d')
        data.index = data['timestamp']
        data['Date'] = data.index

        data = data.sort_index(ascending=True, axis=0)
        new_data = pd.DataFrame(index=range(0, len(data)), columns=['Date', 'Close'])
        for n in range(0, len(data)):
            new_data['Date'][n] = data['Date'][n]
            new_data['Close'][n] = data['Close'][n]

        new_data.index = new_data.Date
        new_data.drop('Date', axis=1, inplace=True)

        dataset = new_data.values
        self.length = int(len(dataset) * (1 - self.valid))
        train2 = dataset
        valid2 = dataset[self.length:, :]

        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(dataset)
        x_train2, y_train2 = [], []
        for j in range(90, len(train2)):
            x_train2.append(scaled_data[j - 90:j, 0])
            y_train2.append(scaled_data[j, 0])
        x_train2, y_train2 = np.array(x_train2), np.array(y_train2)

        x_train2 = np.reshape(x_train2, (x_train2.shape[0], x_train2.shape[1], 1))

        # create and fit the LSTM network
        model2 = Sequential()
        model2.add(LSTM(units=50, return_sequences=True, input_shape=(x_train2.shape[1], 1)))
        model2.add(LSTM(units=50))
        model2.add(Dense(1))

        model2.compile(loss='mean_squared_error', optimizer='adam')
        model2.fit(x_train2, y_train2, epochs=1, batch_size=1, verbose=2)

        inputs = new_data[len(new_data) - len(valid2) - 90:].values
        inputs = inputs.reshape(-1, 1)
        inputs = scaler.transform(inputs)

        X_test3 = []
        for x in range(90, inputs.shape[0]):
            X_test3.append(inputs[x - 90:x, 0])
        X_test3 = np.array(X_test3)

        X_test3 = np.reshape(X_test3, (X_test3.shape[0], X_test3.shape[1], 1))
        closing_price3 = model2.predict(X_test3)
        closing_price3 = scaler.inverse_transform(closing_price3)
        rms3 = np.sqrt(np.mean(np.power((valid2 - closing_price3), 2)))

        self.logging.info('RMSE value on validation set:' + 'Lag = ' + str(90) + ':{}'.format(rms3))
        print('\n RMSE value on validation set:' + 'Lag = ' + str(90))
        print(rms3)
        MAPE2 = np.mean(
            np.abs(np.array(valid2) - np.array(closing_price3) / np.array(closing_price3)))

        train2 = new_data
        valid2 = new_data[self.length:]
        valid2['Predict_Twitter'] = closing_price3

        t2 = []
        t2.append(rms3)
        t2.append(MAPE2)
        total['90'] = t2
        # produce object
        fig8 = go.Figure()
        fig8.update_layout(width=1000,height=700,title='LSTM \n Using Lag' + str(90) + ' RMSE ' + "{0:.2f}".format(rms3),
                           yaxis=go.layout.YAxis(
                               title=go.layout.yaxis.Title(
                                   text="Price",
                                   font=dict(
                                       family="Courier New, monospace",
                                       size=18,
                                       color="#7f7f7f"
                                   )
                               )
                           ))
        btc_train = go.Scatter(x=train2.index, y=train2['Close'], name='History')
        btc_test = go.Scatter(x=valid2.index, y=valid2['Close'], name='Actual')
        btc_test_ = go.Scatter(x=valid2.index, y=valid2['Predict_Twitter'], name='Predictions')
        fig8.add_trace(btc_train)
        fig8.add_trace(btc_test)
        fig8.add_trace(btc_test_)
        self.info['LSTM'] = total
        with open('../JSON/LSTM' + str(90) + '.json', 'w') as outfile:
            json.dump(fig8, outfile, cls=plotly.utils.PlotlyJSONEncoder)
        self.logging.info('LSTM Models have been saved!')
        gc.collect()

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self.info