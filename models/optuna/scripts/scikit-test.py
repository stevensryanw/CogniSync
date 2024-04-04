#Lets create a torch test file for ryan.csv
#Our data dimmentions (11, 1) and the categorization variable has 5 categories

import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

#Lets load the data
data_full = pd.read_csv('ryan.csv')
#First 11 columns are the data
data = data_full.iloc[:, 0:11]
#Last column is the category
labels = data_full.iloc[:, 11]

#Need to encode labels
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

# #Lets convert the data to a tensor
# data_tensor = torch.tensor(data.values, dtype=torch.float32)
# labels_tensor = torch.tensor(labels, dtype=torch.long)

models = {
    #'SVC': SVC(),
    'LDA': LinearDiscriminantAnalysis(),
    'LRC': LogisticRegression(),
    'DTC': DecisionTreeClassifier(),
    'RFC': RandomForestClassifier()
}

param_grids = {
    'LDA': {'solver': ['svd', 'lsqr', 'eigen'], 'shrinkage': [None, 'auto']},
    'LRC': {'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'], 'penalty': ['l1', 'l2']},
    'DTC': {'criterion': ['gini', 'entropy'], 'splitter': ['best', 'random']},
    'RFC': {'n_estimators': [10, 100, 1000], 'criterion': ['gini', 'entropy'], 'max_features': ['auto', 'sqrt', 'log2'],  'max_depth': [None, 10, 100, 1000]}
}

#Lets split the data
X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

#Lets grid search the models with each of their parameters but make it a function to return the best 5 models for each model type and its accuracy score and parameters
def grid_search_models(models, param_grids, data, labels):
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
    best_models = {}
    for model in models:
        print(f'Grid searching {model}')
        start_time = time.time()
        clf = GridSearchCV(models[model], param_grids[model], cv=5, n_jobs=-1)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        end_time = time.time()
        best_models[model] = {'accuracy': accuracy_score(y_test, y_pred), 'precision': precision_score(y_test, y_pred), 'recall': recall_score(y_test, y_pred), 'f1_score': f1_score(y_test, y_pred), 'parameters': clf.best_params_, 'time': end_time - start_time}
        print(f'Accuracy for {model}: {accuracy_score(y_test, y_pred)}')
    return best_models

best_models = grid_search_models(models, param_grids, data, labels)

print(best_models)


# #Lets grid search the models with each of their parameters
# for model in models:
#     print(f'Grid searching {model}')
#     clf = GridSearchCV(models[model], param_grids[model], cv=5, n_jobs=-1)
#     clf.fit(X_train, y_train)
#     y_pred = clf.predict(X_test)
#     print(f'Accuracy for {model}: {accuracy_score(y_test, y_pred)}')


# #Lets grid search the models
# for model in models:
#     print(f'Grid searching {model}')
#     clf = GridSearchCV(models[model], {}, cv=5, n_jobs=-1)
#     clf.fit(X_train, y_train)
#     y_pred = clf.predict(X_test)
#     print(f'Accuracy for {model}: {accuracy_score(y_test, y_pred)}')

