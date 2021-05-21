import pandas as pd
import numpy as np
import datetime

#Data handeling
data = pd.read_csv('/home/ubuntu/DE2_Project/ci_cd/development_server/1000repDataNew.csv')

#Handeling the Time stamps removing hours, minutes and seconds 
time_columns = ['created_at','updated_at','pushed_at']
for i in time_columns:
    data[i] =  data[i].apply(lambda x : x.replace('T',' ').replace('Z',''))
    data[i+'day']= data[i].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%Y%m%d')).astype(int)

#Handeling the reponame, description taking the length of the description as a feature instead of the string 
string_columns = ['reponame','full_name','login']
for i in string_columns:
    data[i+'Length'] = data[i].apply(lambda x :len(x))
#Handeling the description string for some reason didnt want to do as the rest string values.
data ['LenOfDescription'] = data['description'].apply(lambda x : str(x))
data ['LenOfDescription'] = data ['LenOfDescription'].apply(lambda x : len(x))
#Handeling the language string
def languageTranslate(x):
    if x=='JavaScript':
        return 1
    elif x=='Python':
        return 2
    elif x=='Java':
        return 3
    elif x=='Objective-C':
        return 4
    elif x=='Ruby':
        return 5
    elif x=='PHP': 
        return 6
    elif x=='C++':
        return 7
    elif x=='Shell':
        return 8
    elif x=='Go':
        return 9
    elif x=='Dart':
        return 10
    elif x=='TypeScript':
        return 11
    elif x=='Swift':
        return 12
    elif x=='Scala':
        return 13
    elif x=='HTML':
        return 14
    elif x=='Jypyter Notebook':
        return 15
    elif x=='Rust':
        return 16
    else:
        return 0
data['languageNumber'] =  data['language'].apply(lambda x :languageTranslate(x))

#Handeling the license string
data['licenseNumber'] =  data['license'].apply(lambda x :0 if x=='Other' else 1)

#Selecting the features important and with correlation. 
transformed_data = data.drop(columns=['created_at','updated_at','pushed_at','description',
                                      'language','reponame','full_name','login', 'license', 'type','archived', 'updated_atday'])
transformed_data.to_csv('preprosessedData.csv', index = False)

#CORRELATION = transformed_data.corr('spearman')
#print (CORRELATION)
#From Spearmans coefficiants we can se that the columns updated_atday, archived and type has no correlation and will therefore be removed 
