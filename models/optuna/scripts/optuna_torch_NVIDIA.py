import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import torch
import optuna

deviceM1 = 'cuda'
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
data_tensor = torch.tensor(data.values, dtype=torch.float32).cuda()
labels_tensor = torch.tensor(labels, dtype=torch.long).cuda()

params = {
    'n_layers': [3, 4, 5, 6],
    'n_units_l0': [100, 200, 300, 400, 500],
    'n_units_l1': [100, 200, 300, 400, 500],
    'n_units_l2': [100, 200, 300, 400, 500],
    'dropout_l0': [0.1, 0.2, 0.3, 0.4, 0.5],
    'dropout_l1': [0.1, 0.2, 0.3, 0.4, 0.5],
    'dropout_l2': [0.1, 0.2, 0.3, 0.4, 0.5],
    'lr': [0.1, 0.01, 0.001, 0.0001, 0.00001],
    'weight_decay': [0.01, 0.001, 0.0001, 0.00001],
    'batch_size': [16, 32, 64, 128],
    'epochs': [10, 50, 100, 200]
}

# Using Optuna to find the best hyperparameters for each model our training data is 11 columns and our labels are 1 column
def objective(trial):
    X_train, X_test, y_train, y_test = train_test_split(data_tensor, labels_tensor, test_size=0.2, random_state=42)
    X_train = X_train.cuda()
    X_test = X_test.cuda()
    y_train = y_train.cuda()
    y_test = y_test.cuda()

    n_layers = trial.suggest_categorical('n_layers', params['n_layers'])
    n_units_l0 = trial.suggest_categorical('n_units_l0', params['n_units_l0'])
    n_units_l1 = trial.suggest_categorical('n_units_l1', params['n_units_l1'])
    n_units_l2 = trial.suggest_categorical('n_units_l2', params['n_units_l2'])
    dropout_l0 = trial.suggest_categorical('dropout_l0', params['dropout_l0'])
    dropout_l1 = trial.suggest_categorical('dropout_l1', params['dropout_l1'])
    dropout_l2 = trial.suggest_categorical('dropout_l2', params['dropout_l2'])
    lr = trial.suggest_categorical('lr', params['lr'])
    weight_decay = trial.suggest_categorical('weight_decay', params['weight_decay'])
    batch_size = trial.suggest_categorical('batch_size', params['batch_size'])
    epochs = trial.suggest_categorical('epochs', params['epochs'])

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
    ).cuda()

    loss_fn = torch.nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)

    train = torch.utils.data.TensorDataset(X_train, y_train)
    train_loader = torch.utils.data.DataLoader(dataset=train, batch_size=batch_size, shuffle=True)

    for epoch in range(epochs):
        for i, (X, y) in enumerate(train_loader):
            y_pred = model(X)
            loss = loss_fn(y_pred, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # Pruning
            if trial.should_prune():
                raise optuna.TrialPruned()

        print(f'Trial {trial.number}, Epoch: {epoch}, Loss: {loss.item()}')

    with torch.no_grad():
        y_pred = model(X_test)
        loss = loss_fn(y_pred, y_test)
        accuracy = (y_pred.argmax(dim=1) == y_test).float().mean()
        return accuracy
    
# Create a study
study = optuna.create_study(direction='maximize', study_name='pytorch_nn', storage='sqlite:///pytorch_nn.db.sqlite3', load_if_exists=True)
study.optimize(objective, n_trials=100, n_jobs=1, show_progress_bar=True)
