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

# In this class we call all the function of our 
# six model and to produce all the Sentiment for
#  comparison to a dataframe named Comparison.json
import os, pickle
import pandas as pd
import gc
import logging
from datetime import datetime, timedelta, date, time as dtime
gc.enable()
def load_pickle(filepath):
    documents_f = open(filepath, 'rb')
    file = pickle.load(documents_f)
    documents_f.close()
    return file



#Rearrange model information
two_simple = []
x = load_pickle(os.path.join('info.p'))
two_simple.append(x[2]['MA'][0])
two_simple.append(x[4]['ARIMA'][0])
data = {'RMSE': two_simple}
df = pd.DataFrame(data, index=['MA', 'ARIMA'])

two_simple2 = []
two_simple2.append(x[0]['Linear']['GT'][0])
two_simple2.append(x[1]['KNN']['GT'][0])
two_simple2.append(x[3]['SVM']['GT'][0])
data1 = {'RMSE_GT': two_simple2}
df1 = pd.DataFrame(data1, index=['Linear', 'KNN', 'SVM'])
simple2 = []
simple2.append(x[0]['Linear']['N'][0])
simple2.append(x[1]['KNN']['N'][0])
simple2.append(x[3]['SVM']['N'][0])
data2 = {'RMSE_':simple2}
df2 = pd.DataFrame(data2, index =['Linear', 'KNN', 'SVM'])
imple2 = []
imple2.append(x[0]['Linear']['T'][0])
imple2.append(x[1]['KNN']['T'][0])
imple2.append(x[3]['SVM']['T'][0])
data12 = {'RMSE_T':imple2}
df12 = pd.DataFrame(data12, index =['Linear', 'KNN', 'SVM'])
df1 = df2.join(df1)
df1 = df1.join(df12)
df1['RMSE'] = df1.min(axis=1)
imple = []
imple.append(x[5]['LSTM']['30'][0])
data3 = {'RMSE_30':imple}
df3 = pd.DataFrame(data3, index =['LSTM'])
imple = []
imple.append(x[5]['LSTM']['60'][0])
data3 = {'RMSE_60':imple}
df4 = pd.DataFrame(data3, index =['LSTM'])
imple = []
imple.append(x[5]['LSTM']['90'][0])
data3 = {'RMSE_90':imple}
df5 = pd.DataFrame(data3, index =['LSTM'])
df3 = df3.join(df4)
df3 = df3.join(df5)
df3['RMSE'] = df3.min(axis=1)
df = pd.concat([df,df1],sort = True)
df = pd.concat([df,df3],sort = True)
df.fillna(0, inplace= True)
df.to_json(r'../JSON/Comparison.json')
logger.info("Sentiment comparison has been saved.")
gc.collect()



