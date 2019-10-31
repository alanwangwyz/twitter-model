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
# six model and choose one to execute and switch to
#  produce a pickle called name info.p to control 
#  the use of different model.

import gc
import numpy as np
import sys
sys.path.append('..')
from model import Linear
from model.KNN import KNNModel
from model.Moving_Avg import MovingAverage
from model.SVM import SVMmodel
from model.LSTM import LSTMmodel
from model.ARIMA import ARIMAmodel

import logging, pickle, os
np.warnings.filterwarnings('ignore')


def load_pickle(filepath):
    documents_f = open(filepath, 'rb')
    file = pickle.load(documents_f)
    documents_f.close()
    return file

def save_pickle(data, filepath):
    save_documents = open(filepath, 'wb')
    pickle.dump(data, save_documents)
    save_documents.close()

gc.enable()

# log
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('model.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
data = load_pickle(os.path.join('../data/final.p'))
TotalInfo = {}

#initialize all six models
Linear_model = Linear.LinearModel(data, logger)
Linear_model.start()
Linearinfo = Linear_model.join()
TotalInfo[0] = Linearinfo
KNN = KNNModel(data, logger)
KNN.start()
KNNinfo = KNN.join()
TotalInfo[1] = KNNinfo
MA = MovingAverage(data, logger)
MA.start()
MAinfo = MA.join()
TotalInfo[2] = MAinfo
SVM = SVMmodel(data, logger)
SVM.start()
SVMinfo = SVM.join()
TotalInfo[3] = SVMinfo
ARIM = ARIMAmodel(data, logger)
ARIM.start()
ARIMinfo = ARIM.join()
TotalInfo[4] = ARIMinfo
LSTMm = LSTMmodel(data, logger)
LSTMm.start()
LSTinfo = LSTMm.join()
TotalInfo[5] = LSTinfo

# save all the model info into info.p
save_pickle(TotalInfo, os.path.join('info.p'))
gc.collect()



