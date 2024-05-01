#------------------ Importing Libraries -----------------
'''Pytorch'''
import torch
import torch.nn as nn
import torch.nn.functional as F
'''Scikit-learn models'''
from sklearn.svm import SVC
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
'''Tensorflow'''
#import keras
'''Scoring'''
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
'''Data splitting'''
from sklearn.model_selection import train_test_split
#------------------ Importing Libraries -----------------

#------------------ SciKit-Learn ------------------------
def BCI_sklearn_SVC(data, labels):
    """
    Trains a Support Vector Classifier (SVC) model using the provided data and labels.
    
    Parameters:
        data (array-like): The input data for training the model.
        labels (array-like): The corresponding labels for the input data.
        
    Returns:
        float: The score of the trained model on the test data.
    """
    #train and test set created
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    clf = BaggingClassifier(estimator=SVC(), n_jobs=-1)
    clf.fit(trainData, trainLabel)
    return scoring(clf, testData, testLabel)

def BCI_sklearn_RandomForestClassifier(data, labels):
    """
    Trains a Random Forest Classifier model using the provided data and labels.

    Parameters:
    - data: The input data for training the model.
    - labels: The corresponding labels for the input data.

    Returns:
    - The score of the trained model on the test data.

    """
    #train and test set created
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    #optimized parameters are set
    max_depth = 810
    min_samples_split = 4
    min_samples_leaf = 2
    criterion = 'log_loss'
    n_estimators = 960
    max_features = 'log2'
    bootstrap = False
    model = RandomForestClassifier(max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, 
                                   criterion=criterion, n_estimators=n_estimators, max_features=max_features, bootstrap=bootstrap, n_jobs=-1)
    model.fit(trainData, trainLabel)
    return scoring(model, testData, testLabel)

def BCI_sklearn_DecisionTreeClassifier(data, labels):
    """
    Trains a Decision Tree Classifier model using the provided data and labels.

    Parameters:
    - data: The input data for training the model.
    - labels: The corresponding labels for the input data.

    Returns:
    - The score of the trained model on the test data.

    """
    #train and test set created
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    #optimized parameters are set
    max_depth = 628
    min_samples_split = 3
    min_samples_leaf = 2
    max_features = None
    splitter = 'best'
    criterion = 'entropy'
    model = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, 
                                   max_features=max_features, splitter=splitter, criterion=criterion)
    model.fit(trainData, trainLabel)
    return scoring(model, testData, testLabel)

def BCI_sklearn_LogisticRegression(data, labels):
    """
    Trains a logistic regression model using the provided data and labels.

    Parameters:
    - data: The input data for training the model.
    - labels: The corresponding labels for the input data.

    Returns:
    - The score of the trained model on the test data.

    """
    #train and test set created
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    #optimized parameters are set
    C = 1.0
    class_weight = None
    dual = False
    fit_intercept = True
    intercept_scaling = 1
    l1_ratio = None
    max_iter = 100
    multi_class = 'auto'
    n_jobs = -1
    penalty = 'l2'
    random_state = None
    solver = 'saga'
    tol = 0.0001
    verbose = 0 
    warm_start = False
    model = LogisticRegression(C=C, class_weight=class_weight, dual=dual, fit_intercept=fit_intercept, intercept_scaling=intercept_scaling, 
                               l1_ratio=l1_ratio, max_iter=max_iter, multi_class=multi_class, n_jobs=n_jobs, penalty=penalty, random_state=random_state, 
                               solver=solver, tol=tol, verbose=verbose, warm_start=warm_start)
    model.fit(trainData, trainLabel)
    return scoring(model, testData, testLabel)

def BCI_sklearn_GradientBoostingClassifier(data, labels):
    """
    Trains a Gradient Boosting Classifier model on the given data and labels.

    Parameters:
    data (array-like): The input data for training the model.
    labels (array-like): The target labels for training the model.

    Returns:
    float: The score of the trained model on the test data.

    """
    #train and test set created
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    model = GradientBoostingClassifier()
    model.fit(trainData, trainLabel)
    return scoring(model, testData, testLabel)

def BCI_sklearn_KNeighborsClassifier(data, labels):
    """
    Trains a K-Nearest Neighbors classifier using the provided data and labels.
    
    Parameters:
        data (array-like): The input data for training the classifier.
        labels (array-like): The corresponding labels for the input data.
        
    Returns:
        float: The score of the trained model on the test data.
    """
    #train and test set created
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    model = KNeighborsClassifier()
    model.fit(trainData, trainLabel)
    return scoring(model, testData, testLabel)

def BCI_sklearn_GaussianNB(data, labels):
    """
    Trains a Gaussian Naive Bayes classifier using the provided data and labels.
    
    Parameters:
        data (array-like): The input data for training the classifier.
        labels (array-like): The target labels for the input data.
        
    Returns:
        float: The score of the trained model on the test data.
    """
    #train and test set created
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    model = GaussianNB()
    model.fit(trainData, trainLabel)
    return scoring(model, testData, testLabel)

def BCI_sklearn_MLPClassifier(data, labels):
    """
    Trains and evaluates a Multi-Layer Perceptron (MLP) classifier for Brain-Computer Interface (BCI) data.

    Parameters:
    - data (array-like): The input data for training and testing the classifier.
    - labels (array-like): The corresponding labels for the input data.

    Returns:
    - float: The accuracy score of the trained model on the test data.

    """
    #train and test set created
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    model = MLPClassifier()
    model.fit(trainData, trainLabel)
    return scoring(model, testData, testLabel)

def BCI_sklearn_LinearDiscriminantAnalysis(data, labels):
    """
    Perform Linear Discriminant Analysis (LDA) classification on the given data.

    Parameters:
    - data (array-like): The input data for training and testing the LDA model.
    - labels (array-like): The corresponding labels for the input data.

    Returns:
    - float: The score of the trained LDA model on the test data.

    """
    #train and test set created
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    #optimized parameters are set
    solver = 'svd'
    shrinkage = None
    store_covariance = False
    tol = .17029486954279227
    covariance_estimator = None
    model = LinearDiscriminantAnalysis(solver=solver, shrinkage=shrinkage, store_covariance=store_covariance, 
                                       tol=tol, covariance_estimator=covariance_estimator)
    model.fit(trainData, trainLabel)
    return scoring(model, testData, testLabel)

def BCI_sklearn_QuadraticDiscriminantAnalysis(data, labels):
    """
    Perform Quadratic Discriminant Analysis (QDA) classification on the given data.

    Parameters:
    - data (array-like): The input data for training and testing the model.
    - labels (array-like): The corresponding labels for the input data.

    Returns:
    - float: The score of the trained model on the test data.

    """
    #train and test set created
    trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
    #optimized parameters are set
    priors = None
    reg_param = 0.01
    store_covariance = True
    tol = 4.401500018303662e-06
    model = QuadraticDiscriminantAnalysis(priors=priors, reg_param=reg_param, store_covariance=store_covariance, tol=tol)
    model.fit(trainData, trainLabel)
    return scoring(model, testData, testLabel)
#------------------ SciKit-Learn ------------------------

#------------------ PyTorch -----------------------------
def BCI_pytorch_Net(data, labels):
    """
    Trains a PyTorch neural network model for BCI (Brain-Computer Interface) classification.

    Args:
        data (list): A list of input data samples.
        labels (list): A list of corresponding labels for the input data samples.

    Returns:
        tuple: A tuple containing the model's score on the test data and the trained model itself.
    """
    #Checking for mps then cuda then cpu
    try:
        device_usable = torch.device("cuda" if torch.cuda.is_available() else "mps")
    except:
        device_usable = torch.device("cpu")
    #Parameters
    batch_size = 128 
    dropout_l0 = 0.2
    dropout_l1 = 0.1
    dropout_l2 = 0.5
    epochs = 200	
    lr = 0.00001
    n_layers = 6
    n_units_l0 = 300
    n_units_l1 = 300
    n_units_l2 = 300
    weight_decay = 0.00001
    #Finding number of data dimensions for the model
    data_dim = len(data[0])
    #Sending data and labels to tensors
    data_tensor = torch.tensor(data, dtype=torch.float32).to(torch.device(device_usable))
    labels_tensor = torch.tensor(labels, dtype=torch.long).to(torch.device(device_usable))
    #Splitting the data
    X_train, X_test, y_train, y_test = train_test_split(data_tensor, labels_tensor, test_size=0.2)
    #Creating our model
    model = torch.nn.Sequential(
        torch.nn.Linear(data_dim, n_units_l0),
        torch.nn.ReLU(),
        torch.nn.Dropout(dropout_l0),
        torch.nn.Linear(n_units_l0, n_units_l1),
        torch.nn.ReLU(),
        torch.nn.Dropout(dropout_l1),
        torch.nn.Linear(n_units_l1, n_units_l2),
        torch.nn.ReLU(),
        torch.nn.Dropout(dropout_l2),
        torch.nn.Linear(n_units_l2, 5)
    ).to(torch.device(device_usable))

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    #Training the model
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        output = model(X_train)
        loss = criterion(output, y_train)
        loss.backward()
        optimizer.step()
    testData = X_test
    testLabel = y_test
    return scoring(model, testData, testLabel), model
#------------------ PyTorch -----------------------------

#------------------ Tensorflow --------------------------
# def BCI_tensorflow_Net(data, labels):
#     """
#     Trains and evaluates a TensorFlow neural network model for binary classification.

#     Args:
#         data (numpy.ndarray): The input data for training and testing the model.
#         labels (numpy.ndarray): The corresponding labels for the input data.

#     Returns:
#         list: A list containing the test accuracy score and the model parameters.

#     """
#     #train and test set created
#     trainData, testData, trainLabel, testLabel = train_test_split(data, labels, test_size=0.2)
#     #model layer creation
#     model = keras.Sequential([
#     # Adjust the input shape based on your data
#     keras.layers.Input(shape=(11,)),
#     keras.layers.Dense(64, activation='relu'),
#     keras.layers.Dense(32, activation='relu'),
#     # Output layer with sigmoid activation for binary classification
#     keras.layers.Dense(1, activation='sigmoid')
#     ])
#     model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
#     history = model.fit(trainData, trainLabel, epochs=10, batch_size=32)
#     trainPred = model.predict(trainData)
#     #training accuracy calculated
#     correctTrain = 0
#     for i in range(len(trainPred)):
#         if trainPred[i] >= 0.5 and trainLabel[i] == 1:
#             correctTrain += 1
#         elif trainPred[i] < 0.5 and trainLabel[i] == 0:
#             correctTrain += 1
#         else:
#             continue
#     print('Training accuracy:', correctTrain/len(trainPred))
#     testPred = model.predict(testData)
#     correctTest = 0
#     #test accuracy calculated
#     for i in range(len(testPred)):
#         if testPred[i] >= 0.5 and testLabel[i] == 1:
#             correctTest += 1
#         elif testPred[i] < 0.5 and testLabel[i] == 0:
#             correctTest += 1
#         else:
#             continue
#     print('Test accuracy:', correctTest/len(testPred))
#     score = correctTest/len(testPred)
#     parameters = {"Type": "Sequential", "Node 1":"Dense, 64, relu", "Node 2":"Dense, 32, relu", "Node 3":"Dense, 1, sigmoid"}
#     return [score, parameters] 
#------------------ Tensorflow --------------------------

#------------------ Scoring -----------------------------
def scoring(model, x, y):
    """
    Calculate the accuracy, F1 score, precision, and recall of a given model's predictions.

    Parameters:
    model (torch.nn.modules.container.Sequential or sklearn.base.BaseEstimator): The model to evaluate.
    x (array-like): The input data.
    y (array-like): The target labels.

    Returns:
    list: A list containing the accuracy, F1 score, precision, recall, and the model itself.

    """
    #scoring split by model type
    if type(model) == torch.nn.modules.container.Sequential:
        model.eval()
        preds = model(x).argmax(dim=1)
        acc = accuracy_score(y.cpu(), preds.cpu())
        f1 = f1_score(y.cpu(), preds.cpu(), average='macro')
        precision = precision_score(y.cpu(), preds.cpu(), average='macro')
        recall = recall_score(y.cpu(), preds.cpu(), average='macro')
    #scikit-learn scoring
    else:
        preds = model.predict(x)
        acc = accuracy_score(y, preds)
        f1 = f1_score(y, preds, average='macro')
        precision = precision_score(y, preds, average='macro')
        recall = recall_score(y, preds, average='macro')
    return [acc, f1, precision, recall, model]
#------------------ Scoring -----------------------------