#Python script for the model_bci to execute sklearn functions
#Examples: SVC, RandomForestClassifier, GradientBoosting Classifier  KNeighborsClassifier, GaussianNB, MLPClassifier, LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis

import sklearn
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.model_selection import GridSearchCV

def BCI_sklearn(model, data, labels):
    model = model.fit(data, labels)
    return model

def BCI_sklearn_grid_search(model, data, labels, param_grid, cv):
    return GridSearchCV(model, param_grid, cv=cv)

def BCI_sklearn_predict(model, data):
    return model.predict(data)

def BCI_sklearn_predict_proba(model, data):
    return model.predict_proba(data)

def BCI_sklearn_score(model, data, labels):
    return model.score(data, labels)

def BCI_sklearn_cross_val_score(model, data, labels, cv):
    return cross_val_score(model, data, labels, cv=cv)

def BCI_sklearn_cross_val_predict(model, data, labels, cv):
    return cross_val_predict(model, data, labels, cv=cv)

def BCI_sklearn_confusion_matrix(model, data, labels):
    return confusion_matrix(labels, model.predict(data))

def BCI_sklearn_classification_report(model, data, labels):
    return classification_report(labels, model.predict(data))