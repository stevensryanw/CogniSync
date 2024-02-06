#Python script for the model_bci to execute tensorflow functions
import pandas as pd
import os
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

def BCI_tensorflow_sequential(data, labels, name):
    #Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
    model = keras.Sequential([
        keras.layers.Input(shape=(11,)),  # Adjust the input shape based on your data
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')  # Output layer with sigmoid activation for binary classification
    ])
    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    # Convert Pandas Series to NumPy arrays
    y_train = y_train.to_numpy()
    y_test = y_test.to_numpy()
    history = model.fit(X_train, y_train, epochs=10, batch_size=32)
    # Evaluate the model's training error
    trainPred = model.predict(X_train)
    correctTrain = 0
    for i in range(len(trainPred)):
        if trainPred[i] >= 0.5 and y_train[i] == 1:
            correctTrain += 1
        elif trainPred[i] < 0.5 and y_train[i] == 0:
            correctTrain += 1
        else:
            continue
    print('Training accuracy:', correctTrain/len(trainPred))
    # Evaluate the model's test error
    testPred = model.predict(X_test)
    correctTest = 0
    for i in range(len(testPred)):
        if testPred[i] >= 0.5 and y_test[i] == 1:
            correctTest += 1
        elif testPred[i] < 0.5 and y_test[i] == 0:
            correctTest += 1
        else:
            continue
    print('Test accuracy:', correctTest/len(testPred))

    #Save the model
    model.save(name, '_model.h5')

# #Need to go back 1 directory to get to the data
# os.chdir("/BCI_GUI/data/processed")

# data = pd.read_csv('blinksFiltered.csv')
# labels = pd.read_csv('blinksFilteredLabels.csv')

# BCI_tensorflow_sequential(data, labels, 'test')