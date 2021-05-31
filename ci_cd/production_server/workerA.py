import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
import joblib
from celery import Celery

from numpy import loadtxt
import numpy as np
from keras.models import model_from_json
from keras.models import Sequential

import tensorflow as tf
from tensorflow.keras import datasets, models, layers 
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
from tensorflow.keras.models import load_model


#the data file name!
data_file = 'preprosessedData.csv'
#the model name we load!
model = 'rfc_model.m'

def load_data():
    data = pd.read_csv(data_file)
    # list 10 data
    X = data.drop(columns=['stargazers_count'])
    X = X.sample(n= 100, random_state = 1)
    y = data['stargazers_count'].astype(int)
    y = y.sample(n= 100, random_state = 1)
    #y = list(map(int, y))
    #y = np.asarray(y, dtype=np.uint8)
    return X, y


def load_model():
    loaded_model = joblib.load(model)
    return loaded_model

#Neural Network 
def DenseModel():
    model = models.Sequential()
    model.add(Dense(128,input_dim=15, activation='relu'))
    model.add(Dropout(0.3))    
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(20, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(10, activation='relu'))
    model.add(Dense(1))
    
    model.compile(loss='mean_squared_error', optimizer='adam')
    
    return model


# if the best model is Neraul network
def load_NN_Model():
  estimator = KerasRegressor(build_fn=DenseModel, nb_epoch=200, epochs=10, batch_size=25, verbose=True)
  estimator.model = load_model("NN_model.h5")  
  return estimator

# Celery configuration
CELERY_BROKER_URL = 'pyamqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('workerA',broker=CELERY_BROKER_URL,backend=CELERY_RESULT_BACKEND)

@celery.task
def get_predictions():
    results ={}
    X, y = load_data()
    loaded_model = load_model()
    predictions = loaded_model.predict(X)
    results['y'] = y.tolist()
    results['predicted'] =[]
    # print ('results[y]:', results['y'])
    for i in range(len(results['y'])):
        print('%s => %f (expected %f)' % (X[i:i+1].values.tolist(), predictions[i], y[i:i+1]))
        results['predicted'].append(predictions[i].tolist())
    return results

@celery.task
def get_accuracy():
    X, y = load_data()
    loaded_model = load_model()
    predictions = loaded_model.predict(X)
    test_score = mean_squared_error(y, predictions, squared= False)
    print ('RMSE:', test_score)
    return test_score
