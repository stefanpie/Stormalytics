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



df1 = pd.read_csv("dataset.csv")
df2 = pd.read_csv("dataset2.csv")
df = pd.concat([df1, df2])


df.drop(['station_id', 'station_name', 'station_lat', 'station_lon', 'station_elevation', 'time_start', 'filename'], axis=1, inplace=True)

# scaler = MinMaxScaler()
# df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
# print(df)
# input("stopped...")

x = df.drop('is_tornado_present', axis=1)  
y = df['is_tornado_present']
print(x.shape)
input("stopped...")

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.20, random_state=0)

model = GradientBoostingClassifier(n_estimators=500, max_depth = 5, random_state = 0, verbose=11)
model.fit(x_train, y_train)
score = model.score(x_test, y_test)
print(score*100)

y_pred = model.predict(x_test)
print(confusion_matrix(y_test, y_pred))  
print(classification_report(y_test,y_pred))

filename = './finalized_model.save'
pickle.dump(model, open(filename, 'wb'))