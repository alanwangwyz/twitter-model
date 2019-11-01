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

#This part we just call the function 'pyramid.arim'
# to get the Autoregressive Integrated Moving 
# Average model apply to the gov sentiment analysis
#  and to produce the ARIMA.json as the result.

import gc
from pyramid.arima import auto_arima
import plotly
import plotly.graph_objs as go
from fastai.structured import *
import threading
gc.enable()

class ARIMAmodel(threading.Thread):
    def __init__(self, data, logging):
        threading.Thread.__init__(self)
        self.data = data
        self.logging = logging
        self.valid = 0.2
        self.length = 0
        self.info = {}

    def run(self):
        self.logging.info('ARIMA')
        data = self.data
        self.length = int(len(data) * (1 - self.valid))
        train = data
        valid = data[self.length:]
        training = train['Close']
        # build model
        model = auto_arima(training, start_p=1, start_q=1, max_p=3, max_q=3, m=12, start_P=0, seasonal=True, d=1, D=1,
                           trace=True, error_action='ignore', suppress_warnings=True)
        model.fit(training)
        forecast = model.predict(n_periods=len(valid))
        forecast = pd.DataFrame(forecast, index=valid.index, columns=['Prediction'])
        # evaluation
        rms1 = np.sqrt(np.mean(np.power((np.array(valid['Close']) - np.array(forecast['Prediction'])), 2)))
        print('\n RMSE value on validation set:')
        print(rms1)
        MAPE1 = np.mean(np.abs(np.array(valid['Close']) - np.array(forecast['Prediction']) / np.array(forecast['Prediction'])))
        self.logging.info('MAPE value on validation set: {}.'.format(MAPE1))
        print('MAPE value on validation set:')
        print(MAPE1)
        total = []
        total.append(rms1)
        total.append(MAPE1)
        self.info['ARIMA'] = total

        # produce graph
        fig4 = go.Figure()
        fig4.update_layout(width=1000,height=700,title='ARIMA RMSE: \t' + "{0:.2f}".format(rms1), yaxis=go.layout.YAxis(
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
        btc_test_ = go.Scatter(x=forecast.index, y=forecast['Prediction'], name='Predictions')
        fig4.add_trace(btc_train)
        fig4.add_trace(btc_test)
        fig4.add_trace(btc_test_)
        with open('../JSON/ARIMA.json', 'w') as outfile:
            json.dump(fig4, outfile, cls=plotly.utils.PlotlyJSONEncoder)
        self.logging.info('ARIMA has been saved!')

        gc.collect()

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self.info
