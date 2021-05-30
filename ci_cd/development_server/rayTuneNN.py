from ray import tune
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
#from sklearn.model_selection import cross_validate, cross_val_score
from sklearn.preprocessing import StandardScaler
#import sklearn.preprocessing as skl_pre
from sklearn.metrics import r2_score, mean_squared_error

import tensorflow as tf
from tensorflow.keras import datasets, models, layers 
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
seed = 67
#Collect the preprossesed data. 
data = pd.read_csv('preprosessedData.csv')
X = data.drop(columns=['stargazers_count'])
y = data['stargazers_count'].astype(int)
X = StandardScaler().fit_transform(X)
#splitting the data in a testset and a training set 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=seed)

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

#Neural Network 
def DenseModel(config):
    first = config['first']
    second = config['second']
    third = config['third']
    fourth = config['fourth']
    model = models.Sequential()
    model.add(Dense(first,input_dim=15, activation='relu'))
    model.add(Dropout(0.3))    
    model.add(Dense(second, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(third, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(fourth, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def trainModel(config):

    for i in range(10):

       # estimator = KerasRegressor(build_fn=DenseModel(config), nb_epoch=200, epochs=10, batch_size=25, verbose=True)
        estimator = DenseModel(config)
        NN = estimator.fit(X_train, y_train)
        test_predNeural = estimator.predict(X_test)

        test_scoreNeuralNetwork = mean_squared_error(y_test, test_predNeural, squared= False)

        tune.report(mean_loss =test_scoreNeuralNetwork)
    

analysis = tune.run(
    trainModel,
    config={
        "first": tune.grid_search([128]),
        "second": tune.grid_search([100, 128]),       
        'third': tune.grid_search([90,100]),
        'fourth': tune.grid_search([40,50])
    })



print("Best config: ", analysis.get_best_config(
    metric="mean_loss", mode="min"))

# Get a dataframe for analyzing trial results.
df = analysis.results_df
