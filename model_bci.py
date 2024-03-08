#Script for gui_bci to model data in the gui, using our own models
from models.bci_sklearn import *
#from models.bci_pytorch import *
from models.bci_tensorflow import *
# from models.bci_tensorflow import *
import numpy
from sklearn.metrics import accuracy_score
import tensorflow as tf
from tensorflow import keras

#Sklearn models
def BCI_sklearn_SVC(data, labels):
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    print('data split up')
    model = SVC(cache_size=10000)
    print('model created')
    model.fit(trainData, trainLabel)
    print('model fitted')
    parameters = model.get_params()
    print('parameters received')
    score = accuracy_score(testLabel, model.predict(testData))
    print('score received')
    print("Model Accuracy:")
    print(score)
    print("Model Parameters:")
    print(parameters)
    return [score, parameters]

def BCI_sklearn_RandomForestClassifier(data, labels):
    model = RandomForestClassifier()
    return BCI_sklearn(model, data, labels)

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
    model = LinearDiscriminantAnalysis()
    model.fit(trainData, trainLabel)
    parameters = model.get_params()
    score = accuracy_score(testLabel, model.predict(testData))
    print("Model Accuracy:")
    print(score)
    print("Model Parameters:")
    print(parameters)
    return [score, parameters]

def BCI_sklearn_QuadraticDiscriminantAnalysis(data, labels):
    model = QuadraticDiscriminantAnalysis()
    return BCI_sklearn(model, data, labels)

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
