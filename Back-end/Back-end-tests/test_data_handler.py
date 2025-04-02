import torch
import pytest
from data_handler import split_train_test, process_heart_disease_data

def test_split_train_test():
    x = torch.randn(100, 10)  # Dummy feature data
    y = torch.randint(0, 2, (100, 1)).float()  # Dummy binary labels

    x_train, y_train, x_test, y_test = split_train_test(x, y, test_ratio=0.3)

    assert len(x_train) + len(x_test) == 100
    assert len(y_train) + len(y_test) == 100
    assert 0.25 < len(x_test) / len(x) < 0.35  # Test ratio check

def test_process_heart_disease_data():
    with pytest.raises(Exception, match="No dataset uploaded"):
        process_heart_disease_data(None)
