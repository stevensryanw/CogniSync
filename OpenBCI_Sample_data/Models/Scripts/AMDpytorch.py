#Open blinks and jaw clench txt files, /Users/ryanstevens/Documents/OpenBCI_GUI/Sample_Data/OpenBCI_GUI-v5-blinks-jawClench-alpha.txt
import time
time_start = time.time()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split, StratifiedKFold
from skorch import NeuralNetClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

print("PyTorch Version:", torch.__version__)
print("CUDA Available:", torch.cuda.is_available())
#List available devices for pytorch
gpus = [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
for i in gpus:
    print(i)
#List available CPUs for pytorch
print(torch.device('cpu'))
print("Current device", torch.cuda.current_device())

#Data

#Blinks
data = pd.read_csv('OpenBCI_GUI-v5-blinks-jawClench-alpha_copy.txt', sep=",", header=None)

#Removing columns 12-22
data = data.drop(data.columns[12:22], axis=1)
#Remove the first 1000 samples
data = data.drop(data.index[0:1000])
#Reindex the data
data = data.reset_index(drop=True)

#Create a dataframe for the data, columns 1-11
useful_data = data.iloc[:,1:12]

#Create alpha labels, columns 9-11
alphaLabels = data.iloc[:,9:12]

#Create a 1d dataframe of the alphas summed
alphaSum = alphaLabels.mul([9,10,11]).sum(axis=1)

#Plot alpha labels
alphaLabels.plot()

#Ploting the data
useful_data.plot()

n_samps = 21491
n_blinks = 40
lenRangeDown = 30
lenRangeUp = 60
labels = pd.DataFrame()

#Append 21491 norm labels to the dataframe
for i in range(n_samps):
    labels = labels._append(['norm'])

#Generate random blink labels
for _ in range(n_blinks):
    # Randomly select the start and end indices for each blink
    start_idx = random.randint(0, n_samps - lenRangeUp)
    end_idx = start_idx + random.randint(lenRangeDown, lenRangeUp)
    
    # Set the blink labels for the selected range
    for i in range(start_idx, end_idx):
        labels.iloc[i] = 'blink'

labels.value_counts()

#Set labels up for pytorch
labels = labels.replace({'norm': 0, 'blink': 1})

torchData = useful_data.copy()
torchLabels = labels.copy()

#Model
# Modify your model class to accept hyperparameters
class Classifier(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(Classifier, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, 1)  # Output is a binary classification, so one output unit

    def forward(self, x):
        x = nn.functional.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x

# Define your training loop as a function
def train_and_evaluate(model, X_train, y_train, X_test, y_test, epoch_num, batch_size, loss_fn, optimizer):
    start_time = time.time()
    for _ in range(epoch_num):
        model.train()
        for i in range(0, len(X_train), batch_size):
            inputs = torch.tensor(X_train[i:i + batch_size], dtype=torch.float32, device=torch.device('cuda'))
            labels = torch.tensor(y_train[i:i + batch_size], dtype=torch.float32, device=torch.device('cuda'))

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        test_inputs = torch.tensor(X_test, dtype=torch.float32, device=torch.device('cuda'))
        predictions = model(test_inputs)
        predicted_labels = (predictions > 0.5).float()
        accuracy = accuracy_score(y_test, predicted_labels.cpu().numpy())
    
    end_time = time.time()
    return accuracy, end_time - start_time

# Split the data into training and testing sets (80/20%)
train_data, test_data, train_labels, test_labels = train_test_split(torchData, torchLabels, test_size=0.2, random_state=42)
train_data = train_data.to_numpy()
train_labels = train_labels.to_numpy()
test_data = test_data.to_numpy()
test_labels = test_labels.to_numpy()

# Convert your data into PyTorch tensors
train_data_tensor = torch.tensor(train_data, dtype=torch.float32)
# Reshape the data tensor
train_data_tensor = train_data_tensor.view(-1, 11)

train_labels_tensor = torch.tensor(train_labels)
train_labels_tensor = train_labels_tensor.view(-1)

test_data_tensor = torch.tensor(test_data, dtype=torch.float32)

from sklearn.model_selection import ParameterGrid

parameter_grid = {
    'epoch_num': [10, 20, 30],
    'batch_size': [32, 64, 128],
    'hidden_size': [32, 64, 128],
    'loss': [nn.BCELoss(), nn.MSELoss(), nn.CrossEntropyLoss()],
    #'lr': [0.0001, 0.001, 0.01, 0.1],
}

results = []
device = torch.device('cuda')
for params in ParameterGrid(parameter_grid):
    model = Classifier(input_size=11, hidden_size=params['hidden_size'])
    model.to(device)
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    loss = params['loss']
    accuracy, time_taken = train_and_evaluate(model, train_data, train_labels, test_data, test_labels, params['epoch_num'], params['batch_size'], loss, optimizer)
    results.append((params, accuracy, time_taken))
    print("Model Parameters:", params)
    print("Accuracy:", accuracy)
    print("Time taken:", time_taken)



#Output
#Listing results for pytorch
resultsPD = pd.DataFrame(results)
resultsPD.columns = ['runDevice', 'epochNum', 'batchSize', 'loss', 'hiddenSize', 'time', 'trainAccuracy']
resultsPD = resultsPD.sort_values(by=['accuracy'], ascending=False)
resultsPD



#Time
time_end = time.time()
print('Time elapsed:', time_end - time_start, 'seconds')