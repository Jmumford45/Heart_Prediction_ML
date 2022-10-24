#necesary libraries
from pickle import dump, load
import pandas as pd
#library for scaling data
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

#function: loads the file into a dataframe and returns it
def loadData(csv):
    data = pd.read_csv(csv)
    return data

#f() pickles the data 
def pklData(file, df):
    with open(file, 'wb') as f:
        dump(df, f)

#separates our data into categorical and numerical features
def categorical_features(data):
    cat_features = data.select_dtypes(include='object').columns
    #store in list for encoding
    cat_f = cat_features.to_list()
    num_features = data.select_dtypes(include=['int64', 'float64']).columns.to_list()
    return cat_f, num_features

def getDummyDf(df):
    data_origin = df.copy()
    
    df['Sex'].dtype
    if df['Sex'].dtype != 'int64':
        df['Sex'] = df['Sex'].replace(to_replace=['M', 'F'], value=[1,0])
        
    if df['ExerciseAngina'].dtype != 'int64':
        df['ExerciseAngina'] = df['ExerciseAngina'].replace(to_replace=['N', 'Y'], value=(0,1))
        
    df = pd.get_dummies(df)
    return df

def preprocessing(X,y):
    #split the data using simple train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=13)

    print(X_train.shape, X_test.shape)
    print(y_train.shape, y_test.shape)
    
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    X_test_sc = pd.DataFrame(X_test_scaled, columns = X.columns)
    X_train_sc = pd.DataFrame(X_train_scaled, columns = X.columns)
    
    return X_test_sc, X_train_sc, y_train, y_test, scaler

#pickle the original data, pickle the transformed data to train model on

#load the csv file from path
data = loadData('heart.csv')
#pkl the original data for any possible change later
pklData('heart.pkl', data)

categorical = []
numeric = []
if len(categorical) == 0:
    categorical, numeric = categorical_features(data)

dummy_data = getDummyDf(data)
pklData('scaledData.pkl', dummy_data)