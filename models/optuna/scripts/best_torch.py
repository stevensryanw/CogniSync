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

import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score
import torch
import torch.nn as nn
import torch.nn.functional as F

deviceM1 = 'mps'
torch.device(deviceM1)

# Lets load the data
data_full = pd.read_csv('../../../data/ryan.csv')
# First 11 columns are the data
data = data_full.iloc[:, 0:11]
# Last column is the category
labels = data_full.iloc[:, 11]

# Need to encode labels
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

#Turn the data into a tensor
data_tensor = torch.tensor(data.values, dtype=torch.float32).to(torch.device(deviceM1))
labels_tensor = torch.tensor(labels, dtype=torch.long).to(torch.device(deviceM1))

#Split the data
X_train, X_test, y_train, y_test = train_test_split(data_tensor, labels_tensor, test_size=0.2, random_state=42)

#Creating our model to train and test 80/20 split

model = torch.nn.Sequential(
        torch.nn.Linear(11, n_units_l0),
        torch.nn.ReLU(),
        torch.nn.Dropout(dropout_l0),
        torch.nn.Linear(n_units_l0, n_units_l1),
        torch.nn.ReLU(),
        torch.nn.Dropout(dropout_l1),
        torch.nn.Linear(n_units_l1, n_units_l2),
        torch.nn.ReLU(),
        torch.nn.Dropout(dropout_l2),
        torch.nn.Linear(n_units_l2, 5)
    ).to(torch.device(deviceM1))


criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)

#Training the model
model.train()

for epoch in range(epochs):
    optimizer.zero_grad()
    y_pred = model(X_train)
    loss = criterion(y_pred, y_train)
    loss.backward()
    optimizer.step()
    if epoch % 10 == 0:
        print(f'Epoch: {epoch}, Loss: {loss.item()}')
        #Printing accuracy
        
#Testing the model and printing Loss, Accuracy, Precision, Recall, and F1 score
model.eval()

with torch.no_grad():
    y_val = model(X_test)
    loss = criterion(y_val, y_test)
    print(f'Loss: {loss.item()}')
    _, predicted = torch.max(y_val, 1)
    total = predicted.size(0)
    correct = sum(predicted.data.cpu().numpy() == y_test.data.cpu().numpy())
    print(f'Accuracy: {100 * correct / total}%')
    print(f'Precision: {precision_score(y_test.data.cpu().numpy(), predicted.data.cpu().numpy(), average="macro")}')
    print(f'Recall: {recall_score(y_test.data.cpu().numpy(), predicted.data.cpu().numpy(), average="macro")}')
    print(f'F1: {f1_score(y_test.data.cpu().numpy(), predicted.data.cpu().numpy(), average="macro")}')

# Save the model
torch.save(model, 'best_torch.pt')