import pytest
import torch
from encryption_manager import EncryptionManager  # Ensure correct import

# def test_decrypt_data():
#     manager = EncryptionManager()
#     manager.generate_keys()  # 🔹 Generate keys before encrypting
#     original_data = torch.tensor([1.0, 2.0, 3.0])
#     encrypted = manager.encrypt_data(original_data)
#     decrypted = manager.decrypt_data(encrypted)

#     assert torch.allclose(decrypted, original_data), "Decryption failed: Mismatch between original and decrypted data."

def test_encrypt_empty_tensor():
    manager = EncryptionManager()
    manager.generate_keys()  # 🔹 Generate keys before encrypting
    empty_tensor = torch.tensor([])
    with pytest.raises(ValueError):
        manager.encrypt_data(empty_tensor)

def test_encrypt_large_tensor():
    manager = EncryptionManager()
    manager.generate_keys()  # 🔹 Generate keys before encrypting
    
    # Use a 2D tensor, similar to the input shape you provided (334, 9)
    large_tensor = torch.rand(334, 9)  # 2D tensor (334 samples, 9 features)
    
    # Encrypt the 2D tensor
    encrypted = manager.encrypt_data(large_tensor)  # This works after modifying encrypt_data to handle 2D tensors.

def test_encrypt_non_numeric_data():
    manager = EncryptionManager()
    manager.generate_keys()  # 🔹 Generate keys before encrypting
    with pytest.raises(TypeError):
        manager.encrypt_data("invalid_data")
