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

import tensorflow as tf
from tensorflow.keras import datasets, models, layers 
from tensorflow.keras.layers import Dense, Dropout
from keras.wrappers.scikit_learn import KerasRegressor
seed = 67
#Collect the preprossesed data. 
data = pd.read_csv('preprosessedData.csv')
X = data.drop(columns=['stargazers_count'])
y = data['stargazers_count'].astype(int)
X = StandardScaler().fit_transform(X)
#splitting the data in a testset and a training set 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=seed)


#Randomforest 
rfc = RandomForestRegressor(n_jobs = -1, random_state=seed)
rfc.fit(X_train,y_train)
#Pickla modellen
RFC_pickle = pickle.dumps(rfc)

train_predRFC = rfc.predict(X_train)
test_predRFC = rfc.predict(X_test)

training_scoreRFC= mean_squared_error(y_train, train_predRFC, squared=False)
test_scoreRFC = mean_squared_error(y_test, test_predRFC,squared=False)
print("RFC training score RSME ", training_scoreRFC)
print("RFC test score RSME: ", test_scoreRFC)

#Neural Network 
def DenseModel():
    model = models.Sequential()
    model.add(Dense(128,input_dim=15, activation='relu'))
    model.add(Dropout(0.3))    
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.4))
    #model.add(Dense(100, activation='relu'))
    #model.add(Dropout(0.4))
    #model.add(Dense(80, activation='relu'))
    #model.add(Dropout(0.4))
    #model.add(Dense(60, activation='relu'))
    #model.add(Dropout(0.4))   
    #model.add(Dense(40, activation='relu'))
    #model.add(Dropout(0.4))
    model.add(Dense(20, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(10, activation='relu'))
    #model.add(Dropout(0.1))
    model.add(Dense(1))
    
    model.compile(loss='mean_squared_error', optimizer='adam')
    
    return model

estimator = KerasRegressor(build_fn=DenseModel, nb_epoch=200, epochs=10, batch_size=25, verbose=True)

NN = estimator.fit(X_train, y_train)

train_predNeural = estimator.predict(X_train)
test_predNeural = estimator.predict(X_test)

training_scoreNeuralNetwork = mean_squared_error(y_train, train_predNeural, squared= False)
test_scoreNeuralNetwork = mean_squared_error(y_test, test_predNeural, squared= False)
print("RMSE testeing score on Neural network", test_scoreNeuralNetwork)

#Gradient Boosting Regressor
GBR = GradientBoostingRegressor(verbose = 1, n_estimators = 400);
gbr = GBR.fit(X_train , y_train);

#Use pickle.loads(GBR_pickle) to access 
GBR_pickle = pickle.dumps(gbr)

GBR_predTrain=GBR.predict(X_train)
GBR_predTest=GBR.predict(X_test)

training_scoreGBR = mean_squared_error(y_train, GBR_predTrain, squared= False)
test_scoreGBR = mean_squared_error(y_test, GBR_predTest, squared= False)

print("RMSE training score GBR: ", training_scoreGBR)
print("RMSE test score GBR: ", test_scoreGBR)


#This needs to be improved to send away the model and how that model will be implemented. 
#I dont know if you can pickle a tensorflow model other wise send it as a json like Salman did. 

if test_scoreRFC < test_scoreGBR:
    print(test_scoreRFC)
else:
    print(test_scoreGBR)
        


