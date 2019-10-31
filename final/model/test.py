import pandas as pd
import os,pickle
def load_pickle(filepath):
    documents_f = open(filepath, 'rb')
    file = pickle.load(documents_f)
    documents_f.close()
    return file

a = load_pickle(os.path.join("final.p"))
a.to_json(r'../JSON/SentimentChange.json')