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

# This part we combine the numpy and threading
#  accoring to the definition to calculate the
#   moving average to get the Moving average 
#   model apply to the gov sentiment analysis 
#   and to produce the 'MovingAverage.json' as 
#   the result.
import gc
import plotly
import plotly.graph_objs as go
import threading
import json
import numpy as np
gc.enable()
class MovingAverage(threading.Thread):
    def __init__(self, data, logging):
        threading.Thread.__init__(self)
        self.data = data
        self.logging = logging
        self.valid = 0.2
        self.length = 0
        self.info = {}


    def run(self):
        data = self.data
        self.length = int(len(data) * (1 - self.valid))
        train = data
        test = data[self.length:]
        preds = []
        for i in range(0, test.shape[0]):
            a = train['Close'][len(train) - len(test) + i:].sum() + sum(preds)
            b = a / len(test)
            preds.append(b)

        # Evaluation
        rms = np.sqrt(np.mean(np.power((np.array(test['Close']) - preds), 2)))
        self.logging.info('RMSE value on validation set: {}.'.format(rms))
        print('\n RMSE value on validation set:')
        print(rms)
        MAPE = np.mean(np.abs(np.array(test['Close']) - np.array(preds) / np.array(test['Close'])))
        self.logging.info('MAPE value on validation set: {}.'.format(MAPE))
        print('MAPE value on validation set:')
        print(MAPE)
        test['Predictions'] = preds
        total = []
        total.append(rms)
        total.append(MAPE)
        self.info['MA'] = total
        
        # produce graph
        fig = go.Figure()
        fig.update_layout(width=1000,height=700, title='Moving Average \n RMSE'+"{0:.2f}".format(rms), yaxis=go.layout.YAxis(
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
        btc_test = go.Scatter(x=test.index, y=test['Close'], name='Actual')
        btc_test_ = go.Scatter(x=test.index, y=test['Predictions'], name='Predictions')
        fig.add_trace(btc_train)
        fig.add_trace(btc_test)
        fig.add_trace(btc_test_)

        with open('../JSON/MovingAverage.json', 'w') as outfile:
            json.dump(fig, outfile, cls=plotly.utils.PlotlyJSONEncoder)
        self.logging.info('Moving Average have been saved!')

        gc.collect()

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self.info






