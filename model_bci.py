#Script for gui_bci to model data in the gui, using our own models
from models.bci_sklearn import *
#from models.bci_pytorch import *
from models.bci_tensorflow import *
# from models.bci_tensorflow import *
import numpy as np
from sklearn.metrics import accuracy_score
import tensorflow as tf
from tensorflow import keras
import time
from sklearn.model_selection import GridSearchCV
from sklearn.covariance import EmpiricalCovariance
from sklearn.covariance import MinCovDet
from sklearn.covariance import ShrunkCovariance
from sklearn.covariance import LedoitWolf
from joblib import parallel_backend
import random
from sklearn.ensemble import BaggingClassifier
from sklearn.svm import LinearSVC
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

#Sklearn models
def BCI_sklearn_SVC(data, labels):
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    clf = BaggingClassifier(estimator=SVC(), n_jobs=-1)
    t1 = time.time()
    clf.fit(trainData, trainLabel)
    t2 = time.time()
    timeDiff = t2-t1
    print("BaggingSVC took ", timeDiff, "seconds to fit")
    print('model fitted')
    parameters = clf.get_params()
    print('parameters received')
    t3 = time.time()
    score = accuracy_score(testLabel, clf.predict(testData))
    t4 = time.time()
    timeDiff2 = t4-t3
    print("Fitting took ", timeDiff2)
    print('score received')
    print("Model Accuracy:")
    print(score)
    print("Model Parameters:")
    print(parameters)
    return [score, parameters, timeDiff]

def BCI_sklearn_RandomForestClassifier(data, labels):
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    model = RandomForestClassifier(n_jobs=-1)
    #"""
    print('model created')
    t1 = time.time()
    model.fit(trainData, trainLabel)
    t2 = time.time()
    timeDiff = t2-t1
    print("RFC took ", timeDiff, "seconds to fit")
    print('model fitted')
    parameters = model.get_params()
    print('parameters received')
    t3 = time.time()
    score = accuracy_score(testLabel, model.predict(testData))
    t4 = time.time()
    timeDiff2 = t4-t3
    print("Fitting took ", timeDiff2)
    print('score received')
    print("Model Accuracy:")
    print(score)
    print("Model Parameters:")
    print(parameters)
    return [score, parameters]
def BCI_sklearn_DecisionTreeClassifier(data, labels):
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    model = DecisionTreeClassifier()
    print('model created')
    t1 = time.time()
    model.fit(trainData, trainLabel)
    t2 = time.time()
    timeDiff = t2-t1
    parameters = model.get_params()
    t3 = time.time()
    score = accuracy_score(testLabel, model.predict(testData))
    t4 = time.time()
    timeDiff2 = t4-t3
    print("Model Accuracy:")
    print(score)
    print("Model Parameters:")
    print(parameters)
    return [score, parameters]
def BCI_sklearn_LogisticRegression(data, labels):
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    model = LogisticRegression(solver='saga', n_jobs=-1)
    print('model created')
    t1 = time.time()
    model.fit(trainData, trainLabel)
    t2 = time.time()
    timeDiff = t2-t1
    parameters = model.get_params()
    t3 = time.time()
    score = accuracy_score(testLabel, model.predict(testData))
    t4 = time.time()
    timeDiff2 = t4-t3
    print("Model Accuracy:")
    print(score)
    print("Model Parameters:")
    print(parameters)
    return [score, parameters]

def BCI_sklearn_GradientBoostingClassifier(data, labels):
    model = GradientBoostingClassifier()
    return BCI_sklearn(model, data, labels)

def BCI_sklearn_KNeighborsClassifier(data, labels):
    model = KNeighborsClassifier()
    return BCI_sklearn(model, data, labels)

def BCI_sklearn_GaussianNB(data, labels):
    model = GaussianNB()
    return BCI_sklearn(model, data, labels)

def BCI_sklearn_MLPClassifier(data, labels):
    model = MLPClassifier()
    return BCI_sklearn(model, data, labels)

def BCI_sklearn_LinearDiscriminantAnalysis(data, labels):
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    cov = EmpiricalCovariance()
    cov2 = MinCovDet()
    cov3 = ShrunkCovariance()
    cov4 = LedoitWolf()
    model = LinearDiscriminantAnalysis()
    model.fit(trainData, trainLabel)
    parameters = model.get_params()
    preds = model.predict(testData)
    score = accuracy_score(testLabel, preds)
    print("Model Accuracy:")
    print(score)
    print("Model Parameters:")
    print(parameters)
    print(model.get_feature_names_out())
    print(preds)
    return [score, parameters]

def BCI_sklearn_QuadraticDiscriminantAnalysis(data, labels):
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    model = QuadraticDiscriminantAnalysis()
    model.fit(trainData, trainLabel)
    parameters = model.get_params()
    preds = model.predict(testData)
    #print(preds)
    #np.set_printoptions(threshold=thing)
    score = accuracy_score(testLabel, preds)
    print("Model Accuracy:")
    print(score)
    print("Model Parameters:")
    print(parameters)
    return [score, parameters]

#Pytorch models
# def BCI_pytorch_Net(data, labels):
#     model = Net()
#     return BCI_pytorch(model, data, labels)

#Tensorflow models
def BCI_tensorflow_Net(data, labels):
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    model = keras.Sequential([
    keras.layers.Input(shape=(11,)),  # Adjust the input shape based on your data
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')  # Output layer with sigmoid activation for binary classification
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    history = model.fit(trainData, trainLabel, epochs=10, batch_size=32)
    trainPred = model.predict(trainData)
    correctTrain = 0
    for i in range(len(trainPred)):
        if trainPred[i] >= 0.5 and trainLabel[i] == 1:
            correctTrain += 1
        elif trainPred[i] < 0.5 and trainLabel[i] == 0:
            correctTrain += 1
        else:
            continue
    print('Training accuracy:', correctTrain/len(trainPred))
    testPred = model.predict(testData)
    correctTest = 0
    for i in range(len(testPred)):
        if testPred[i] >= 0.5 and testLabel[i] == 1:
            correctTest += 1
        elif testPred[i] < 0.5 and testLabel[i] == 0:
            correctTest += 1
        else:
            continue
    print('Test accuracy:', correctTest/len(testPred))
    score = correctTest/len(testPred)
    parameters = {"Type": "Sequential", "Node 1":"Dense, 64, relu", "Node 2":"Dense, 32, relu", "Node 3":"Dense, 1, sigmoid"}
    return [score, parameters]
