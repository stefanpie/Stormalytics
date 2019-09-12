import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, HuberRegressor, BayesianRidge, Lasso, ElasticNet, Ridge
from sklearn.neural_network import MLPRegressor


from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import r2_score, mean_squared_error

from pyproj import Geod
import matplotlib.pyplot as plt
from matplotlib import collections  as mc


import datetime


pd.set_option('display.max_columns', 500)


df = pd.read_csv('./hurdat2_processed.csv')
df = df[df.system_status == 'HU']



df = pd.concat([df,pd.get_dummies(df['system_status-12'], prefix='system_status-12')],axis=1)
df = pd.concat([df,pd.get_dummies(df['system_status-6'], prefix='system_status-6')],axis=1)
df = pd.concat([df,pd.get_dummies(df['system_status'], prefix='system_status')],axis=1)
df = pd.concat([df,pd.get_dummies(df['system_status+6'], prefix='system_status+24')],axis=1)
df = pd.concat([df,pd.get_dummies(df['system_status+24'], prefix='system_status+24')],axis=1)


for col in df.columns: 
    print(col) 

input_features = ['year', 'month', 'day',
				  'hour', 'minute',
				  'longitude', 'latitude',
				  'max_sus_wind', 'min_pressure',
				  'delta_distance', 'azimuth',
				  'year-6', 'month-6', 'day-6',
				  'hour-6', 'minute-6',
				  'longitude-6', 'latitude-6',
				  'max_sus_wind-6', 'min_pressure-6',
				  'delta_distance-6', 'azimuth-6',
				  'year-12', 'month-12', 'day-12',
				  'hour-12', 'minute-12',
				  'longitude-12', 'latitude-12',
				  'max_sus_wind-12', 'min_pressure-12',
				  'delta_distance-12', 'azimuth-12',
				  'day_of_year', 'minute_of_day',
				  'day_of_year-6', 'minute_of_day-6',
				  'day_of_year-12', 'minute_of_day-12',
				  'aday','aday-6','aday-12',
				  'x','y',
				  'x-6','y-6',
				  'x-12','y-12',
				  'vpre','vpre-6','vpre-12',
				  'landfall','landfall-6','landfall-12']
for col in df.columns:
    if 'system_status-12_' in col or 'system_status-6_' in col or 'system_status_' in col:
            input_features.append(col)
output_features = ['latitude+24', 'longitude+24', 'max_sus_wind+24', 'min_pressure+24']

for col in df.columns: 
    print(col) 

print(df)

x = np.array(df[input_features].values.tolist())
y = np.array(df[output_features].values.tolist())

scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()

x_scaled = scaler_x.fit_transform(x)
y_scaled = scaler_y.fit_transform(y)

x_train, x_test, y_train, y_test = train_test_split(x_scaled, y_scaled, test_size=0.3, random_state=42)

linear = LinearRegression()
lasso = Lasso()
ridge = Ridge()
elastic = ElasticNet()
b_ridge = BayesianRidge(verbose=True)
huber = HuberRegressor()
svr = SVR(verbose=True, tol=0.001, kernel ='rbf')
gb = GradientBoostingRegressor(n_estimators = 500, max_depth = 5, verbose = 1)
mlp_reg = MLPRegressor((128,128,128,64,32), activation='relu',
					   verbose=True,max_iter=200,
					   tol=0.0000001,
					   learning_rate='adaptive')

multi = MultiOutputRegressor(linear)

multi.fit(x_train, y_train)
y_pred = multi.predict(x_test)

y_test = scaler_y.inverse_transform(y_test)
y_pred = scaler_y.inverse_transform(y_pred)

print(y_test)
print(y_pred)

results = np.hstack((y_test,y_pred))
results_df = pd.DataFrame(results)
results_df.columns = ['lat_test', 'lon_test', 'max_sus_wind_test', 'min_pressure_test',
					  'lat_pred', 'lon_pred', 'max_sus_wind_pred', 'min_pressure_pred']


wgs84_geod = Geod(ellps='WGS84')
def delta_distance_azimuth(lat1,lon1,lat2,lon2):
	az12, az21, dist = wgs84_geod.inv(lon1,lat1,lon2,lat2)
	dist = [x / 1000.0 for x in dist]
	return dist


results_df['error_distance'] = delta_distance_azimuth(results_df['lat_test'].tolist(),results_df['lon_test'].tolist(),results_df['lat_pred'].tolist(),results_df['lon_pred'].tolist())
results_df['error_wind'] = results_df['max_sus_wind_pred']-results_df['max_sus_wind_test']
results_df['error_pressure'] = results_df['min_pressure_pred']-results_df['min_pressure_test']



print(results_df)


# # Plot feature importance
# feature_importance = multi.estimators_[0].feature_importances_
# # make importances relative to max importance
# feature_importance = 100.0 * (feature_importance / feature_importance.max())
# sorted_idx = np.argsort(feature_importance)[-10:]

# pos = np.arange(sorted_idx.shape[0]) + .5
# plt.subplot(1, 2, 2)
# plt.barh(pos[-10:], feature_importance[sorted_idx], align='center')
# plt.yticks(pos[-10:], np.array(input_features)[sorted_idx])
# plt.xlabel('Relative Importance')
# plt.title('Feature Importance')
# plt.show()

data = []
for i in results_df.values.tolist()[:]:
    data.append( [ (i[1], i[0]), (i[5], i[4]) ] )

lc = mc.LineCollection(data, colors='b', linewidths=1)
fig, ax = plt.subplots()
ax.add_collection(lc)
ax.autoscale()
ax.margins(0.1)
plt.show()

results_df.boxplot(column=['error_distance'])
plt.show()

results_df.boxplot(column=['error_wind'])
plt.show()

results_df.boxplot(column=['error_pressure'])
plt.show()
