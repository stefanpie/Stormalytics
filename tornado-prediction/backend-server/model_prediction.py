import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import MinMaxScaler
import csv
from sklearn.ensemble import GradientBoostingClassifier
import pickle
import json


model_filename = "./finalized_model.save"
loaded_model = pickle.load(open(model_filename, 'rb'))

data_in_df = pd.read_csv("recent_scans_processed.csv")
station_ids = data_in_df["station_id"].values
data_in_df.drop(['station_id', 'station_name', 'station_lat', 'station_lon', 'station_elevation', 'time_start'], axis=1, inplace=True)

model_in  = np.asarray(data_in_df)

y_pred = loaded_model.predict_proba(model_in)
print(y_pred[:,1])
print(station_ids)

dictionary = dict(zip(station_ids, y_pred[:,1]))
print(dictionary)


with open('./prediction.json', 'w') as fp:
    json.dump(dictionary, fp)