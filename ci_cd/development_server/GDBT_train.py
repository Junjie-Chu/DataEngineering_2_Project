import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
# from sklearn.model_selection import cross_validate, cross_val_score
from sklearn.preprocessing import StandardScaler
# import sklearn.preprocessing as skl_pre
from sklearn.metrics import r2_score, mean_squared_error
import joblib

seed = 67
# Collect the preprossesed data.
data = pd.read_csv('preprosessedData.csv')
X = data.drop(columns=['stargazers_count'])
y = data['stargazers_count'].astype(int)
X = StandardScaler().fit_transform(X)
# splitting the data in a testset and a training set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=seed)

# Gradient Boosting Regressor
GBR = GradientBoostingRegressor(verbose=1, n_estimators=400)
gbr = GBR.fit(X_train, y_train)

# Use pickle.loads(GBR_pickle) to access
GBR_pickle = pickle.dumps(gbr)
joblib.dump(gbr, "gdbt_model.m")

GBR_predTrain = GBR.predict(X_train)
GBR_predTest = GBR.predict(X_test)

training_scoreGBR = mean_squared_error(y_train, GBR_predTrain, squared=False)
test_scoreGBR = mean_squared_error(y_test, GBR_predTest, squared=False)

print("RMSE training score GBR: ", training_scoreGBR)
print("RMSE test score GBR: ", test_scoreGBR)
