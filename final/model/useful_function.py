from datetime import datetime, timedelta, date, time as dtime
import matplotlib.dates as mdates
from scipy.stats import norm
from fastai.structured import *
import plotly.graph_objs as go

np.warnings.filterwarnings('ignore')
class FunctionalTools():
    def predict(time_interval, model, std, df, type):
        today = date.today()
        end_day = today + timedelta(days=time_interval)
        date_rng = pd.date_range(start=today, end=end_day, freq='D')
        new_data = pd.DataFrame(date_rng, columns=['Date'])
        valid = new_data
        valid.index = new_data['Date']
        if type == 'L' or type == 'K':

            add_datepart(valid, 'Date')
            new_data.drop('Elapsed', axis=1, inplace=True)
            new_data['mon_fri'] = 0

            def check(date):
                if date == 0 or date == 4:
                    return 1
                return 0

            new_data['mon_fri'] = new_data['Dayofweek'].apply(lambda row: check(row))
        elif type == 'SVM':
            valid['Date'] = valid['Date'].map(mdates.date2num)

        # print(df.iloc[-1, df.columns.get_loc("neg")])
        if 'neg' in df.columns:
            valid['neg'] = df.iloc[-1, df.columns.get_loc("neg")]
            valid['pos'] = df.iloc[-1, df.columns.get_loc("pos")]
        if 'Gneg' in df.columns:
            valid['Gneg'] = df.iloc[-1, df.columns.get_loc("Gneg")]
            valid['Gpos'] = df.iloc[-1, df.columns.get_loc("Gpos")]


        # valid = new_data['Date']
        # print(valid)
        y_predict = model.predict(valid)
        new_data['Close'] = y_predict
        # print(new_data)
        ci = norm.interval(0.90, loc=0, scale=1)
        bound = ci[-1]*std
        new_data['Close_High'] = new_data['Close'].apply(lambda x: x + bound)
        new_data['Close_Low'] = new_data['Close'].apply(lambda x: x - bound)
        return new_data

    def plot_intervals(predictions, mid=True, start=None, stop=None, title=None):
        predictions = (
            predictions.loc[start:stop].copy()
            if start is not None or stop is not None
            else predictions.copy()
        )
        data = []

        # Lower trace will fill to the upper trace
        trace_low = go.Scatter(
            x=predictions.index,
            y=predictions["Close_Low"],
            fill="tonexty",
            line=dict(color="rgb(255, 204, 0)"),
            fillcolor="rgba(173, 216, 230, 0.4)",
            showlegend=True,
            name="lower",
        )
        # Upper trace has no fill
        trace_high = go.Scatter(
            x=predictions.index,
            y=predictions["Close_High"],
            fill=None,
            line=dict(color="rgb(255, 204, 0)"),
            showlegend=True,
            name="upper",
        )

        # Must append high trace first so low trace fills to the high trace
        data.append(trace_high)
        data.append(trace_low)

        if mid:
            trace_mid = go.Scatter(
                x=predictions.index,
                y=predictions["Close"],
                fill=None,
                line=dict(color="green"),
                showlegend=True,
                name="Future_predict",
            )
            data.append(trace_mid)

        
        layout = go.Layout(
            width=1000,
            height=700,
            title=dict(text="Prediction Intervals" if title is None else title),
            yaxis=dict(title=dict(text="price")),
            xaxis=dict(
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(count=1, label="1d", step="day", stepmode="backward"),
                            dict(count=7, label="1w", step="day", stepmode="backward"),
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(step="all"),
                        ]
                    )
                ),
                rangeslider=dict(visible=True),
                type="date",
            ),
        )

        fig = go.Figure(data=data, layout=layout)
        # fig["layout"]["font"] = dict(size=20)
        # fig.layout.template = "plotly_white"
        return fig

    def evaluate(name, rms_linear1, train_, valid, valid1, index, fig):
        if index == rms_linear1:

            fig.update_layout(width=1000,height=700,title=name + "{0:.2f}".format(rms_linear1), yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text="Price",
                    font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="#7f7f7f"
                    )
                )
            ))
            btc_train = go.Scatter(x=train_.index, y=train_['Close'], name='History',
                                   line=dict(color="rgb(98,110,250)"))
            btc_test = go.Scatter(x=valid.index, y=valid['Close'], name='Actual', line=dict(color="rgb(239,84,59)"))
            btc_twitter = go.Scatter(x=valid1.index, y=valid1['Predict_Twitter'], name='Twitter_predict',
                                     line=dict(color="rgb(94,212,174)"))
            # btc_twitter = go.Scatter(x=valid1.index, y=valid1['Predict_twitter'], name='Twitter_predict')
            fig.add_trace(btc_train)
            fig.add_trace(btc_test)
            fig.add_trace(btc_twitter)
            # fig2.add_trace(btc_twitter)
            return fig
        else:
            fig2 = go.Figure()
            fig2.update_layout(width=1000,height=700,title=name + "{0:.2f}".format(rms_linear1), yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text="Price",
                    font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="#7f7f7f"
                    )
                )
            ))
            btc_train = go.Scatter(x=train_.index, y=train_['Close'], name='History',
                                   line=dict(color="rgb(98,110,250)"))
            btc_test = go.Scatter(x=valid.index, y=valid['Close'], name='Actual', line=dict(color="rgb(239,84,59)"))
            btc_twitter = go.Scatter(x=valid1.index, y=valid1['Predict_Twitter'], name='Twitter_predict',
                                     line=dict(color="rgb(94,212,174)"))
            # btc_twitter = go.Scatter(x=valid1.index, y=valid1['Predict_twitter'], name='Twitter_predict')
            fig2.add_trace(btc_train)
            fig2.add_trace(btc_test)
            fig2.add_trace(btc_twitter)
            return fig2
            # fig2.add_trace(btc_twitter)
            # fig2.show()








