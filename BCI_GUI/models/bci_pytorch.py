#Python script for the model_bci to execute tensorflow functions

import torch as torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import ParameterGrid
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time

class BCI_pytorch(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(BCI_pytorch, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, 1)  # Output is a binary classification, so one output unit

    def forward(self, x):
        x = nn.functional.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x
    
def load_torch_data(torchData, torchLabels):
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

    return train_data_tensor, train_labels_tensor, test_data_tensor, test_labels
    
def train_and_evaluate(model, X_train, y_train, X_test, y_test, epoch_num, batch_size, loss_fn, optimizer):
    start_time = time.time()
    for _ in range(epoch_num):
        model.train()
        for i in range(0, len(X_train), batch_size):
            inputs = torch.tensor(X_train[i:i + batch_size], dtype=torch.float32, device=torch.device('mps'))
            labels = torch.tensor(y_train[i:i + batch_size], dtype=torch.float32, device=torch.device('mps'))

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optimizer.step()

    model.eval()
    with torch.no_grad():
        test_inputs = torch.tensor(X_test, dtype=torch.float32, device=torch.device('mps'))
        predictions = model(test_inputs)
        predicted_labels = (predictions > 0.5).float()
        accuracy = accuracy_score(y_test, predicted_labels.cpu().numpy())
    
    end_time = time.time()
    return accuracy, end_time - start_time

def run_torch(device, torchData, torchLabels):
    train_data, train_labels, test_data, test_labels = load_torch_data(torchData, torchLabels)

    parameter_grid = {
        'epoch_num': [10, 20, 30],
        'batch_size': [32, 64, 128],
        'hidden_size': [32, 64, 128],
        'loss': [nn.BCELoss(), nn.MSELoss(), nn.CrossEntropyLoss()],
        #'lr': [0.0001, 0.001, 0.01, 0.1],
    }

    results = []
    run_device = torch.device(device)
    for params in ParameterGrid(parameter_grid):
        model = BCI_pytorch(input_size=11, hidden_size=params['hidden_size'])
        model.to(run_device)
        optimizer = optim.SGD(model.parameters(), lr=0.01)
        loss = params['loss']
        accuracy, time_taken = train_and_evaluate(model, train_data, train_labels, test_data, test_labels, params['epoch_num'], params['batch_size'], loss, optimizer)
        results.append((params, accuracy, time_taken))
        print("Model Parameters:", params)
        print("Accuracy:", accuracy)
        print("Time taken:", time_taken)


