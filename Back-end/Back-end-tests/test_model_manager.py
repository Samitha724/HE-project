import torch
from model_manager import LR, train_model

def test_train_model():
    x_train = torch.randn(50, 5)  # Dummy data with 5 features
    y_train = torch.randint(0, 2, (50, 1)).float()

    model = LR(n_features=5)
    trained_model = train_model(model, x_train, y_train, epochs=1)  # 1 epoch for quick testing

    assert isinstance(trained_model, LR)
