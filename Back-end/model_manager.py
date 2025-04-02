
# model_manager.py
import torch

class LR(torch.nn.Module):
    """Linear Regression model with sigmoid activation."""
    
    def __init__(self, n_features):
        super(LR, self).__init__()
        self.lr = torch.nn.Linear(n_features, 1)
        
    def forward(self, x):
        out = torch.sigmoid(self.lr(x))
        return out
    
class EncryptedLR:
    """Encrypted version of the Linear Regression model."""
    
    def __init__(self, torch_lr):
        self.weight = torch_lr.lr.weight.data.tolist()[0]
        self.bias = torch_lr.lr.bias.data.tolist()
        
    def forward(self, enc_x):
        enc_out = enc_x.dot(self.weight) + self.bias
        return enc_out
    
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)

def train_model(model, x_train, y_train, learning_rate=1, epochs=5):
    """
    Train the linear regression model.
    
    Args:
        model (LR): The model to train
        x_train (torch.Tensor): Training features
        y_train (torch.Tensor): Training targets
        learning_rate (float): Learning rate for SGD
        epochs (int): Number of training epochs
        
    Returns:
        LR: Trained model
    """
    optim = torch.optim.SGD(model.parameters(), lr=learning_rate)
    criterion = torch.nn.BCELoss()
    
    for e in range(1, epochs + 1):
        optim.zero_grad()
        out = model(x_train)
        loss = criterion(out, y_train)
        loss.backward()
        optim.step()
        print(f"Loss at epoch {e}: {loss.data}")
    
    return model





# # model_manager.py
# import torch

# class LR(torch.nn.Module):
#     """Linear Regression model with sigmoid activation."""
    
#     def __init__(self, n_features):
#         super(LR, self).__init__()
#         self.lr = torch.nn.Linear(n_features, 1)
        
#     def forward(self, x):
#         # Return raw output for noise analysis
#         return self.lr(x)

# class EncryptedLR:
#     """Encrypted version of the Linear Regression model."""
    
#     def __init__(self, torch_lr):
#         self.weight = torch_lr.lr.weight.data.tolist()[0]
#         self.bias = torch_lr.lr.bias.data.tolist()
        
#     def forward(self, enc_x):
#         enc_out = enc_x.dot(self.weight) + self.bias
#         return enc_out
    
#     def __call__(self, *args, **kwargs):
#         return self.forward(*args, **kwargs)

# def train_model(model, x_train, y_train, learning_rate=1, epochs=5):
#     """
#     Train the linear regression model.
    
#     Args:
#         model (LR): The model to train
#         x_train (torch.Tensor): Training features
#         y_train (torch.Tensor): Training targets
#         learning_rate (float): Learning rate for SGD
#         epochs (int): Number of training epochs
        
#     Returns:
#         LR: Trained model
#     """
#     optim = torch.optim.SGD(model.parameters(), lr=learning_rate)
#     criterion = torch.nn.BCELoss()
    
#     for e in range(1, epochs + 1):
#         optim.zero_grad()
#         out = model(x_train)
#         loss = criterion(out, y_train)
#         loss.backward()
#         optim.step()
#         print(f"Loss at epoch {e}: {loss.data}")
    
#     return model