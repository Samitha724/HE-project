# data_handler.py
import pandas as pd
import torch
import random

def split_train_test(x, y, test_ratio=0.3):
    """
    Split data into training and testing sets.
    
    Args:
        x (torch.Tensor): Feature data
        y (torch.Tensor): Target data
        test_ratio (float): Proportion of data to use for testing
        
    Returns:
        tuple: (x_train, y_train, x_test, y_test)
    """
    idxs = [i for i in range(len(x))]
    random.shuffle(idxs)
    delim = int(len(x) * test_ratio)
    test_idxs, train_idxs = idxs[:delim], idxs[delim:]
    return x[train_idxs], y[train_idxs], x[test_idxs], y[test_idxs]

def process_heart_disease_data(file_path):
    """
    Process the heart disease dataset from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        tuple: (x_train, y_train, x_test, y_test)
    """
    if file_path is None:
        raise Exception("No dataset uploaded")
        
    # Read and preprocess data
    data = pd.read_csv(file_path)
    data = data.dropna()
    data = data.drop(columns=["education", "currentSmoker", "BPMeds", "diabetes", "diaBP", "BMI"])
    
    # Balance data
    grouped = data.groupby('TenYearCHD')
    min_size = grouped.size().min()
    balanced_data = pd.DataFrame()
    
    for name, group in grouped:
        sampled_group = group.sample(n=min_size, random_state=73)
        balanced_data = pd.concat([balanced_data, sampled_group])
    
    data = balanced_data.reset_index(drop=True)
    
    # Extract features and target
    y = torch.tensor(data["TenYearCHD"].values).float().unsqueeze(1)
    data = data.drop(columns=["TenYearCHD"])
    
    # Standardize features
    data = (data - data.mean()) / data.std()
    x = torch.tensor(data.values).float()
    
    return split_train_test(x, y)