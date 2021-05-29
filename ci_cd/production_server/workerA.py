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

#the data file name!
data_file = 'preprosessedData.csv'
#the model name we load!
model = 'gdbt.m'

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
        #print(X[i:i+1].values.tolist())
        #print(predictions[i])
        #print(y[i:i+1])
        results['predicted'].append(predictions[i].tolist())
    # print ('results:', results)
    return results

@celery.task
def get_accuracy():
    X, y = load_data()
    loaded_model = load_model()
    predictions = loaded_model.predict(X)
    test_score = mean_squared_error(y, predictions, squared= False)
    print ('RMSE:', test_score)
    return test_score
