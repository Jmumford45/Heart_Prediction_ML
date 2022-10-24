#save the model for production
import joblib
#modeling libraries
from pickle import load
from sklearn.model_selection import train_test_split, GridSearchCV, learning_curve
from sklearn.ensemble import RandomForestClassifier
#metrics 
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, plot_confusion_matrix
from ETL import getDummyDf, pklData
#custom function from ETL
from ETL import preprocessing
import pandas as pd

#f() unpickle the data and load for modeling
def loadData():
    with open('scaledData.pkl', 'rb') as f:
        df = load(f)
    return df

#f() drop target into its own column
def targetFeature(df, target):
    target_col = df[target]
    if target in df.columns:
        df.drop(labels=target, axis=1, inplace=True)

    X = df.copy()
    y = target_col
    return X, y

#f() split the data into train and test
def dataSplit(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=13)
    return X_train, X_test, y_train, y_test

#f()method to interchangeabley test classifiers
def clfFitPredict(clf, X_train, X_test, y_train, y_test):
    clf.fit(X_train, y_train)
    #print(f"The score for the train set is: {clf.score(X_train, y_train)}")
    #print(f"The score for the test set is: {clf.score(X_test, y_test)}")
    
    y_pred = clf.predict(X_test)
    #print(classification_report(y_test, y_pred))
    
    acc = roc_auc_score(y_test, y_pred)
    #print(f"The accuracy of the model is: {acc}")
    
    #plot_confusion_matrix(clf, X_test, y_test)
    return clf

#f() to save scaled data columns 
def dfColumns(df):
    headers = df.columns
    headers_df = pd.DataFrame(columns=headers)
    return headers_df

#f() to transform json into useable form for model
def pipelineTransform(json, headers):
    if(type(json) == dict):
        df = pd.DataFrame([json])
        print(df)
    else:
        df = pd.read_json(json, orient='index')

    numeric = ['Age', 'RestingBP', 'Cholesterol', 'FastingBS', 'MaxHR', 'Oldpeak']
    for col in df.columns:
        if col in numeric and df[col].dtype == 'object':
            df[col] = pd.to_numeric(df[col])

    df_dumb = getDummyDf(df)
    df_join = df_dumb.merge(headers, how='outer', sort=True)

    if 'HeartDisease' in df_dumb.columns:
        df.join.drop(labels='HeartDisease', axis=1, inplace=True)

    return df_join

#function to reorder joined dataframe from json data into correct order and fillna values
def reorder(df, headers):
    df_reordered = df[headers.columns]
    df_predict = df_reordered.fillna(0)
    return df_predict

data = loadData()

df = data.copy()
X, y = targetFeature(data, 'HeartDisease')

headers_X = dfColumns(X)

#X_train, X_test, y_train, y_test = dataSplit(X,y)
X_test, X_train, y_train, y_test, minMax = preprocessing(X, y)

#hyperparameter tuning for the RFC
#most of the hyperparameter tuning I tried was trial and error, the following were the best parameters that 
#sqeezed some more performance from the model
forest = RandomForestClassifier(max_depth=90, max_features='log2', max_leaf_nodes=50, min_samples_leaf=3, min_samples_split=8,)

forest_clf = clfFitPredict(forest, X_train, X_test, y_train, y_test)

#save model
joblib.dump(forest, 'classifer.joblib')
#save scaler
joblib.dump(minMax, 'scaler.joblib')
#save headers
pklData('headers.pkl', headers_X)
