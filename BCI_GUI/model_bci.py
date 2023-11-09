#Script for gui_bci to model data in the gui, using our own models
from models.bci_sklearn import *
# from models.bci_pytorch import *
# from models.bci_tensorflow import *

#Sklearn models
def BCI_sklearn_SVC(data, labels):
    model = SVC()
    return BCI_sklearn(model, data, labels)

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
    model = LinearDiscriminantAnalysis()
    return BCI_sklearn(model, data, labels)

def BCI_sklearn_QuadraticDiscriminantAnalysis(data, labels):
    model = QuadraticDiscriminantAnalysis()
    return BCI_sklearn(model, data, labels)

#Pytorch models
# def BCI_pytorch_Net(data, labels):
#     model = Net()
#     return BCI_pytorch(model, data, labels)

#Tensorflow models
def BCI_tensorflow_Net(data, labels):
    return BCI_tensorflow_sequential(data, labels)