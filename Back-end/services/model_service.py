import torch
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class ModelService:
    """Service for model training and evaluation."""
    
    def __init__(self):
        self.model = None
        self.encrypted_model = None
        
    def train_model(self, training_data, learning_rate=1, epochs=5):
        """Train the Logistic regression model."""
        x_train, y_train = training_data
        self.model = self._create_model(x_train.shape[1])
        
        optim = torch.optim.SGD(self.model.parameters(), lr=learning_rate)
        criterion = torch.nn.BCELoss()
        
        for e in range(1, epochs + 1):
            optim.zero_grad()
            out = self.model(x_train)
            loss = criterion(out, y_train)
            loss.backward()
            optim.step()
            print(f"Loss at epoch {e}: {loss.data}")
    
    def _create_model(self, n_features):
        """Create a new Logistic regression model."""
        return LR(n_features)
        
    def create_encrypted_model(self):
        """Create encrypted version of the trained model."""
        if self.model is None:
            raise Exception("Model not trained")
            
        self.encrypted_model = EncryptedLR(self.model)
        
    def get_encrypted_model(self):
        """Get the encrypted model."""
        return self.encrypted_model        
   
    def evaluate_plain_metrics(self, x_test, y_test):
        """Evaluate the plain model and return four metrics."""
        self.model.eval()
        with torch.no_grad():
            out = self.model(x_test)
            predicted = (out > 0.5).int()  # Model's output is already probabilities
            y_true = y_test.int().cpu().numpy()
            y_pred = predicted.cpu().numpy()
            return {
                "accuracy": accuracy_score(y_true, y_pred),
                "precision": precision_score(y_true, y_pred, zero_division=0),
                "recall": recall_score(y_true, y_pred, zero_division=0),
                "f1": f1_score(y_true, y_pred, zero_division=0)
            }
        

class LR(torch.nn.Module):
    """Logistic Regression model with sigmoid activation."""
    
    def __init__(self, n_features):
        super(LR, self).__init__()
        self.lr = torch.nn.Linear(n_features, 1)
        
    def forward(self, x):
        out = torch.sigmoid(self.lr(x))
        return out
    
    
class EncryptedLR:
    """Encrypted version of the Logistic Regression model."""
    
    def __init__(self, torch_lr):
        self.weight = torch_lr.lr.weight.data.tolist()[0]
        self.bias = torch_lr.lr.bias.data.tolist()
        
    def forward(self, enc_x):
        enc_out = enc_x.dot(self.weight) + self.bias
        return enc_out
    
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)