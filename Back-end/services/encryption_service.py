import tenseal as ts
from time import time
import torch
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class EncryptionService:
    """Service for encryption operations."""
    
    def __init__(self, user_selected_parameters=None):
        self.ctx_eval = None
        self.encrypted_data = None
        self.user_selected_parameters = user_selected_parameters
        
    def has_context(self):
        """Check if encryption context exists."""
        return self.ctx_eval is not None
        
    def has_encrypted_data(self):
        """Check if encrypted data exists."""
        return self.encrypted_data is not None
        
    def generate_keys(self, poly_mod_degree=4096, coeff_mod_bit_sizes=None):
        """Generate encryption keys with configurable parameters."""
        if coeff_mod_bit_sizes is None:
            coeff_mod_bit_sizes = [40, 20, 40]
        
        # Validate parameters 
        if poly_mod_degree not in [4096, 8192]:
            raise ValueError("Poly mod degree must be 4096 or 8192")  #Function Execution Stops: When raise ValueError(...) is executed, the normal execution of the generate_keys function is immediately interrupted. The remaining lines of code within generate_keys will not be executed.
        
        if len(coeff_mod_bit_sizes) < 2 or any(size > 60 for size in coeff_mod_bit_sizes):
            raise ValueError("Invalid coefficient modulus. Each prime must be ≤ 60 bits")
        
        print(f"Generating keys with poly_mod_degree={poly_mod_degree} and coeff_mod_bit_sizes={coeff_mod_bit_sizes}")  # Add this line

        self.ctx_eval = ts.context(ts.SCHEME_TYPE.CKKS, poly_mod_degree, -1, coeff_mod_bit_sizes)
        self.ctx_eval.global_scale = 2 ** 20
        self.ctx_eval.generate_galois_keys()

        print("Key generation completed")  # Add this line
        
    def encrypt_data(self, x_test):
        """Encrypt test data."""
        if not self.has_context():
            raise Exception("Keys not generated")

        if not isinstance(x_test, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")

        if x_test.numel() == 0:
            raise ValueError("Input tensor is empty")
        
        t_start = time()

        if x_test.ndimension() == 1:
            self.encrypted_data = [ts.ckks_vector(self.ctx_eval, x.tolist()) for x in x_test]
        elif x_test.ndimension() == 2:
            self.encrypted_data = [ts.ckks_vector(self.ctx_eval, row.tolist()) for row in x_test]
        else:
            raise ValueError("Only 1D and 2D tensors are supported for encryption")
        
        t_end = time()
        print(f"Encryption of the test-set took {int(t_end - t_start)} seconds")
        
    def get_encrypted_data(self):
        """Get encrypted data."""
        return self.encrypted_data   

    def encrypted_evaluation(self, model, enc_x_test, y_test):
        """Evaluate the encrypted model and return metrics."""
        t_start = time()
        y_true = []
        y_pred = []
        
        for enc_x, y in zip(enc_x_test, y_test):
            enc_out = model(enc_x)
            # Decrypt the output and apply sigmoid
            out = torch.sigmoid(torch.tensor(enc_out.decrypt()))
            pred = (out > 0.5).int().item()
            y_pred.append(pred)
            y_true.append(y.item())
        
        t_end = time()
        print(f"Evaluated {len(y_true)} entries in {int(t_end - t_start)} seconds")
        
        return {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0)
        }    

    def get_parameter_combinations(self):
        """Generate a list of parameter combinations to test."""
        parameter_dicts = [
            {"poly_mod_degree": 4096, "coeff_mod_bit_sizes": [40, 20, 40]},
            {"poly_mod_degree": 8192, "coeff_mod_bit_sizes": [40, 20, 40]},
        ]

        if self.user_selected_parameters:
            parameter_dicts.append({
                "poly_mod_degree": self.user_selected_parameters["poly_mod_degree"],
                "coeff_mod_bit_sizes": self.user_selected_parameters["coeff_mod_bit_sizes"],
            })

        # Convert dicts to tuples
        return [
            (param["poly_mod_degree"], param["coeff_mod_bit_sizes"])
            for param in parameter_dicts
        ]

    # Inside EncryptionService class
    def set_user_selected_parameters(self, poly_mod_degree, coeff_mod_bit_sizes):
        self.user_selected_parameters = {
            'poly_mod_degree': poly_mod_degree,
            'coeff_mod_bit_sizes': coeff_mod_bit_sizes
        }
    def get_user_selected_parameters(self):
        return self.user_selected_parameters