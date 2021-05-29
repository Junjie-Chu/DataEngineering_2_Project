import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
#from sklearn.model_selection import cross_validate, cross_val_score
from sklearn.preprocessing import StandardScaler
#import sklearn.preprocessing as skl_pre
from sklearn.metrics import r2_score, mean_squared_error

seed = 67
#Collect the preprossesed data. 
data = pd.read_csv('preprosessedData.csv')
X = data.drop(columns=['stargazers_count'])
y = data['stargazers_count'].astype(int)
X = StandardScaler().fit_transform(X)
#splitting the data in a testset and a training set 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=seed)

import joblib
#Randomforest 
rfc = RandomForestRegressor(n_estimators=90,criterion='mse',max_depth=7,min_samples_leaf=1,min_samples_split=2,n_jobs = -1, random_state=seed)
rfc.fit(X_train,y_train)
#Pickla modellen
RFC_pickle = pickle.dumps(rfc)
joblib.dump(rfc, "rfc_model.m")

train_predRFC = rfc.predict(X_train)
test_predRFC = rfc.predict(X_test)

training_scoreRFC= mean_squared_error(y_train, train_predRFC, squared=False)
test_scoreRFC = mean_squared_error(y_test, test_predRFC,squared=False)
print("RFC training score RSME ", training_scoreRFC)
print("RFC test score RSME: ", test_scoreRFC)

