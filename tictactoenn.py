"""This file contains the neural network model to use for the computer player in the game."""

import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
import pickle
import numpy as np

if not torch.backends.mps.is_available():
    if not torch.backends.mps.is_built():
        print("MPS not available because the current PyTorch install was not "
              "built with MPS enabled.")
    else:
        print("MPS not available because the current MacOS version is not 12.3+ "
              "and/or you do not have an MPS-enabled device on this machine.")

else:
    gpu = torch.device("mps")
    print("MPS is available on this machine. Using device: {}".format(gpu))


# Prepare the dataset
# Assuming you have already loaded the dataset and saved it using pickle
with open('tic_tac_toe_dataset.pkl', 'rb') as file:
    dataset = pickle.load(file)


# Split the dataset into training and test sets
train_dataset, test_dataset = train_test_split(dataset, test_size=0.2, random_state=42)

train_data = np.stack([item[0] for item in train_dataset])
train_targets = np.stack([item[1] for item in train_dataset])

test_data = np.stack([item[0] for item in test_dataset])
test_targets = np.stack([item[1] for item in test_dataset])

# Prepare the input and target tensors for training
# Convert numpy arrays to tensors
train_inputs = torch.tensor(train_data, dtype=torch.float, device=gpu)
train_targets = torch.tensor(train_targets, dtype=torch.float, device=gpu)

test_inputs = torch.tensor(test_data, dtype=torch.float, device=gpu)
test_targets = torch.tensor(test_targets, dtype=torch.float, device=gpu)

print("Training data shape: {}".format(train_inputs.shape))
print(train_targets)