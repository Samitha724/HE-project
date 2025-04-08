import pandas as pd
import torch
import random

class DataService:
    """Service for data processing and management."""
    
    def __init__(self):
        self.file_path = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        
    def set_file_path(self, file_path):
        """Set the path to the data file."""
        self.file_path = file_path
        
    def has_file(self):
        """Check if a file path has been set."""
        return self.file_path is not None
        
    def process_data(self):
        """Process the heart disease dataset."""
        if not self.has_file():
            raise Exception("No dataset uploaded")
            
        # Read and preprocess data
        data = pd.read_csv(self.file_path)
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
        
        # Split data
        self.x_train, self.y_train, self.x_test, self.y_test = self._split_train_test(x, y)
        
    def _split_train_test(self, x, y, test_ratio=0.3):
        """Split data into training and testing sets."""
        idxs = [i for i in range(len(x))]
        random.shuffle(idxs)
        delim = int(len(x) * test_ratio)
        test_idxs, train_idxs = idxs[:delim], idxs[delim:]
        return x[train_idxs], y[train_idxs], x[test_idxs], y[test_idxs]
        
    def get_training_data(self):
        """Get training data."""
        return self.x_train, self.y_train
        
    def get_test_features(self):
        """Get test features."""
        return self.x_test
        
    def get_test_targets(self):
        """Get test targets."""
        return self.y_test
