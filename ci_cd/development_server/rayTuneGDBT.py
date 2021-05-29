from ray import tune
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

import ray
ray.init(address='auto', _redis_password='5241590000000000')


seed = 67
#Collect the preprossesed data. 
data = pd.read_csv('preprosessedData.csv')
X = data.drop(columns=['stargazers_count'])
y = data['stargazers_count'].astype(int)
X = StandardScaler().fit_transform(X)

#splitting the data in a testset and a training set 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=seed)

def train_RF(config):
    n_estimators = config['n_estimators']
    criterion = config['criterion']
    max_depth = config['max_depth']
    min_samples_leaf = config['min_samples_leaf']
    min_samples_split = config['min_samples_split']
    for step in range(5):
        rfc = GradientBoostingRegressor(n_estimators= n_estimators,criterion = criterion,max_depth=max_depth, random_state=seed)
        rfc.fit(X_train,y_train)
        
        test_predRFC = rfc.predict(X_test)
        test_scoreRFC = mean_squared_error(y_test, test_predRFC,squared=False)
        tune.report(mean_loss = test_scoreRFC)
    

analysis = tune.run(
    train_RF,
    config={
        "n_estimators": tune.grid_search([100,200,300]),
        "criterion": tune.grid_search(['mse']),       
        'max_depth': tune.grid_search([7,8,9]),
        'min_samples_leaf': tune.grid_search([1,2]),
        'min_samples_split' : tune.grid_search([2,3])
    })



print("Best config: ", analysis.get_best_config(
    metric="mean_loss", mode="min"))

# Get a dataframe for analyzing trial results.
df = analysis.results_df
