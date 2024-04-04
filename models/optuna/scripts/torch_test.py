import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import torch

deviceM1 = 'mps'
torch.device(deviceM1)

# Lets load the data
data_full = pd.read_csv('ryan.csv')
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

# Define the model 11 inputs, 100 hidden units, 1 output
model = torch.nn.Sequential(
    torch.nn.Linear(11, 100),
    torch.nn.ReLU(),
    torch.nn.Linear(100, 100),
    torch.nn.ReLU(),
    torch.nn.Linear(100, 4)
).to(torch.device(deviceM1))

# Loss and optimizer
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Training loop
n_epochs = 100
for epoch in range(n_epochs):
    # Forward pass and loss
    y_pred = model(data_tensor)
    loss = criterion(y_pred, labels_tensor)
    
    # Backward pass and update
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    
    if (epoch+1) % 10 == 0:
        print(f'epoch: {epoch+1}, loss = {loss.item():.4f}')

# Test the model
with torch.no_grad():
    y_pred = model(data_tensor)
    loss = criterion(y_pred, labels_tensor)
    print(f'Loss: {loss:.4f}')
    print(f'Accuracy: {((y_pred.argmax(1) == labels_tensor).sum()/len(labels_tensor))*100:.4f}%')

# Save the model
torch.save(model.state_dict(), 'ryan.ckpt')

