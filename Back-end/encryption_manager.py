#beforeupdate 3-26-25
# # encryption_manager.py
# import tenseal as ts
# from time import time
# import torch

# class EncryptionManager:
#     """Manages encryption operations and context."""
    
#     def __init__(self):
#         self.ctx_eval = None
        
#     def generate_keys(self):
#         """Generate encryption keys and context."""
#         poly_mod_degree = 4096
#         coeff_mod_bit_sizes = [40, 20, 40]
#         self.ctx_eval = ts.context(ts.SCHEME_TYPE.CKKS, poly_mod_degree, -1, coeff_mod_bit_sizes)
#         self.ctx_eval.global_scale = 2 ** 20
#         self.ctx_eval.generate_galois_keys()
        
#     def encrypt_data(self, x_test):
#         """
#         Encrypt test data.
        
#         Args:
#             x_test (torch.Tensor): Test data to encrypt
            
#         Returns:
#             list: Encrypted test data
#         """
#         if self.ctx_eval is None:
#             raise Exception("Keys not generated")

#          # Check if input is a tensor, else raise TypeError#pytest error 11<
#         if not isinstance(x_test, torch.Tensor):
#             raise TypeError("Input must be a torch.Tensor")
#         # Check if input is a tensor, else raise TypeError#pytest error 11<

#         # Check for empty tensor#pytest error 10<
#         if x_test.numel() == 0:
#             raise ValueError("Input tensor is empty")
#         # Check for empty tensor#pytest error 10<    
        
#         t_start = time()

#         #enc_x_test = [ts.ckks_vector(self.ctx_eval, x.tolist()) for x in x_test] #this line replace with below lines error 9
#         # from unit testing tensor dimention error 9 <
#         # Check the dimensionality of the input tensor
#         if x_test.ndimension() == 1:
#             # Encrypt 1D tensor (vector)
#             enc_x_test = [ts.ckks_vector(self.ctx_eval, x.tolist()) for x in x_test]# pytest error 12 replace this line with below
#             # enc_x_test = ts.ckks_vector(self.ctx_eval, x_test.tolist())# pytest error 12
#         elif x_test.ndimension() == 2:
#             # Handle 2D data (encrypt each row)
#             enc_x_test = [ts.ckks_vector(self.ctx_eval, row.tolist()) for row in x_test]
#         else:
#             raise ValueError("Only 1D and 2D tensors are supported for encryption")
#         # from unit testing tensor dimention error 9 >

        
#         t_end = time()
#         print(f"Encryption of the test-set took {int(t_end - t_start)} seconds")
        
#         return enc_x_test

#     def evaluate_model(self, model, enc_x_test, y_test):
#         """
#         Evaluate encrypted model performance.
        
#         Args:
#             model (EncryptedLR): Encrypted model
#             enc_x_test (list): Encrypted test data
#             y_test (torch.Tensor): Test targets
            
#         Returns:
#             float: Accuracy score
#         """
#         correct = 0
#         for enc_x, y in zip(enc_x_test, y_test):
#             enc_out = model(enc_x)
#             out = enc_out.decrypt()
#             out = torch.tensor(out)
#             out = torch.sigmoid(out)
#             if torch.abs(out - y) < 0.5:
#                 correct += 1
#         return correct / len(y_test)


# #3-26- update new 1

# # encryption_manager.py
# import tenseal as ts
# from time import time
# import torch
# import itertools

# class EncryptionManager:
#     """Manages encryption operations and context."""
    
#     def __init__(self):
#         self.ctx_eval = None
        
#     def generate_keys(self):
#         """Generate encryption keys and context."""
#         poly_mod_degree = 4096
#         coeff_mod_bit_sizes = [40, 20, 40]
#         self.ctx_eval = ts.context(ts.SCHEME_TYPE.CKKS, poly_mod_degree, -1, coeff_mod_bit_sizes)
#         self.ctx_eval.global_scale = 2 ** 20
#         self.ctx_eval.generate_galois_keys()
        
#     def encrypt_data(self, x_test):
#         """
#         Encrypt test data.
        
#         Args:
#             x_test (torch.Tensor): Test data to encrypt
            
#         Returns:
#             list: Encrypted test data
#         """
#         if self.ctx_eval is None:
#             raise Exception("Keys not generated")

#          # Check if input is a tensor, else raise TypeError#pytest error 11<
#         if not isinstance(x_test, torch.Tensor):
#             raise TypeError("Input must be a torch.Tensor")
#         # Check if input is a tensor, else raise TypeError#pytest error 11<

#         # Check for empty tensor#pytest error 10<
#         if x_test.numel() == 0:
#             raise ValueError("Input tensor is empty")
#         # Check for empty tensor#pytest error 10<    
        
#         t_start = time()

#         #enc_x_test = [ts.ckks_vector(self.ctx_eval, x.tolist()) for x in x_test] #this line replace with below lines error 9
#         # from unit testing tensor dimention error 9 <
#         # Check the dimensionality of the input tensor
#         if x_test.ndimension() == 1:
#             # Encrypt 1D tensor (vector)
#             enc_x_test = [ts.ckks_vector(self.ctx_eval, x.tolist()) for x in x_test]# pytest error 12 replace this line with below
#             # enc_x_test = ts.ckks_vector(self.ctx_eval, x_test.tolist())# pytest error 12
#         elif x_test.ndimension() == 2:
#             # Handle 2D data (encrypt each row)
#             enc_x_test = [ts.ckks_vector(self.ctx_eval, row.tolist()) for row in x_test]
#         else:
#             raise ValueError("Only 1D and 2D tensors are supported for encryption")
#         # from unit testing tensor dimention error 9 >

        
#         t_end = time()
#         print(f"Encryption of the test-set took {int(t_end - t_start)} seconds")
        
#         return enc_x_test

#     def evaluate_model(self, model, enc_x_test, y_test):
#         """
#         Evaluate encrypted model performance.
        
#         Args:
#             model (EncryptedLR): Encrypted model
#             enc_x_test (list): Encrypted test data
#             y_test (torch.Tensor): Test targets
            
#         Returns:
#             float: Accuracy score
#         """
#         correct = 0
#         for enc_x, y in zip(enc_x_test, y_test):
#             enc_out = model(enc_x)
#             out = enc_out.decrypt()
#             out = torch.tensor(out)
#             out = torch.sigmoid(out)
#             if torch.abs(out - y) < 0.5:
#                 correct += 1
#         return correct / len(y_test)

# #3-26-25 update new 2

# import tenseal as ts
# from time import time
# import torch
# import itertools

# class EncryptionManager:
#     """Manages encryption operations and context."""
    
#     def __init__(self):
#         self.ctx_eval = None
        
#     def generate_keys(self, poly_mod_degree=4096, coeff_mod_bit_sizes=None):
#         """
#         Generate encryption keys with configurable parameters.
        
#         Args:
#             poly_mod_degree (int): Polynomial modulus degree
#             coeff_mod_bit_sizes (list): Coefficient modulus bit sizes
#         """
#         if coeff_mod_bit_sizes is None:
#             coeff_mod_bit_sizes = [40, 20, 40]
        
#             # Validate parameters
#         if poly_mod_degree not in [2048, 4096, 8192]:
#             raise ValueError(f"Invalid poly_mod_degree: {poly_mod_degree}")
#         if len(coeff_mod_bit_sizes) < 3:
#             raise ValueError(f"Invalid coeff_mod_bit_sizes: {coeff_mod_bit_sizes}")

#         self.ctx_eval = ts.context(ts.SCHEME_TYPE.CKKS, poly_mod_degree, -1, coeff_mod_bit_sizes)
#         self.ctx_eval.global_scale = 2 ** 20
#         self.ctx_eval.generate_galois_keys()

#         # Add this validation step here
#         if self.ctx_eval is None:
#             raise Exception("Failed to initialize encryption context")
        
#     def encrypt_data(self, x_test):
#         """
#         Encrypt test data.
        
#         Args:
#             x_test (torch.Tensor): Test data to encrypt
            
#         Returns:
#             list: Encrypted test data
#         """
#         if self.ctx_eval is None:
#             raise Exception("Keys not generated")

#         if not isinstance(x_test, torch.Tensor):
#             raise TypeError("Input must be a torch.Tensor")

#         if x_test.numel() == 0:
#             raise ValueError("Input tensor is empty")
        
#         t_start = time()

#         if x_test.ndimension() == 1:
#             enc_x_test = [ts.ckks_vector(self.ctx_eval, x.tolist()) for x in x_test]
#         elif x_test.ndimension() == 2:
#             enc_x_test = [ts.ckks_vector(self.ctx_eval, row.tolist()) for row in x_test]
#         else:
#             raise ValueError("Only 1D and 2D tensors are supported for encryption")
        
#         t_end = time()
#         print(f"Encryption of the test-set took {int(t_end - t_start)} seconds")
        
#         return enc_x_test

#     def evaluate_model(self, model, enc_x_test, y_test):
#         """
#         Evaluate encrypted model performance.
        
#         Args:
#             model (EncryptedLR): Encrypted model
#             enc_x_test (list): Encrypted test data
#             y_test (torch.Tensor): Test targets
            
#         Returns:
#             float: Accuracy score
#         """
#         correct = 0
#         for enc_x, y in zip(enc_x_test, y_test):
#             enc_out = model(enc_x)
#             out = enc_out.decrypt()
#             out = torch.tensor(out)
#             out = torch.sigmoid(out)
#             if torch.abs(out - y) < 0.5:
#                 correct += 1
#         return correct / len(y_test)
    
#     @staticmethod
#     def get_parameter_combinations():
#         """
#         Generate a list of parameter combinations to test.
        
#         Returns:
#             list: List of parameter combinations
#         """
#         poly_mod_degrees = [4096, 8192]
#         coeff_mod_combinations = [
#             [40, 20, 40]
            
            
#         ]
        
#         return list(itertools.product(poly_mod_degrees, coeff_mod_combinations))

##back to new 1 with a working parameter update ffect 2 files

# import tenseal as ts
# from time import time
# import torch
# import itertools

# class EncryptionManager:
#     """Manages encryption operations and context."""
    
#     def __init__(self):
#         self.ctx_eval = None
        
#     def generate_keys(self, poly_mod_degree=4096, coeff_mod_bit_sizes=None):
#         """
#         Generate encryption keys with configurable parameters.
        
#         Args:
#             poly_mod_degree (int): Polynomial modulus degree
#             coeff_mod_bit_sizes (list): Coefficient modulus bit sizes
#         """
#         if coeff_mod_bit_sizes is None:
#             coeff_mod_bit_sizes = [40, 20, 40]
        
#         self.ctx_eval = ts.context(ts.SCHEME_TYPE.CKKS, poly_mod_degree, -1, coeff_mod_bit_sizes)
#         self.ctx_eval.global_scale = 2 ** 20
#         self.ctx_eval.generate_galois_keys()
        
#     def encrypt_data(self, x_test):
#         """
#         Encrypt test data.
        
#         Args:
#             x_test (torch.Tensor): Test data to encrypt
            
#         Returns:
#             list: Encrypted test data
#         """
#         if self.ctx_eval is None:
#             raise Exception("Keys not generated")

#         if not isinstance(x_test, torch.Tensor):
#             raise TypeError("Input must be a torch.Tensor")

#         if x_test.numel() == 0:
#             raise ValueError("Input tensor is empty")
        
#         t_start = time()

#         if x_test.ndimension() == 1:
#             enc_x_test = [ts.ckks_vector(self.ctx_eval, x.tolist()) for x in x_test]
#         elif x_test.ndimension() == 2:
#             enc_x_test = [ts.ckks_vector(self.ctx_eval, row.tolist()) for row in x_test]
#         else:
#             raise ValueError("Only 1D and 2D tensors are supported for encryption")
        
#         t_end = time()
#         print(f"Encryption of the test-set took {int(t_end - t_start)} seconds")
        
#         return enc_x_test

#     def evaluate_model(self, model, enc_x_test, y_test):
#         """
#         Evaluate encrypted model performance.
        
#         Args:
#             model (EncryptedLR): Encrypted model
#             enc_x_test (list): Encrypted test data
#             y_test (torch.Tensor): Test targets
            
#         Returns:
#             float: Accuracy score
#         """
#         correct = 0
#         for enc_x, y in zip(enc_x_test, y_test):
#             enc_out = model(enc_x)
#             out = enc_out.decrypt()
#             out = torch.tensor(out)
#             out = torch.sigmoid(out)
#             if torch.abs(out - y) < 0.5:
#                 correct += 1
#         return correct / len(y_test)
    
#     @staticmethod
#     def get_parameter_combinations():
#         """
#         Generate a list of parameter combinations to test.
        
#         Returns:
#             list: List of parameter combinations
#         """
#         poly_mod_degrees = [4096, 8192]
#         coeff_mod_combinations = [
#             [40, 20, 40],
#             # [20, 20, 20],  # Valid for poly_mod_degree 4096 and 8192 [cite: 146, 147]
#             # [17, 17],     # Valid for poly_mod_degree 4096 and 8192 [cite: 146, 147]
#             # [30, 20, 30],  # Valid for poly_mod_degree 4096 [cite: 147]
#             # [19, 19, 19],  # Valid for poly_mod_degree 4096 [cite: 147]
#             # [18, 18, 18],  # Valid for poly_mod_degree 4096 [cite: 147]
#             # [18, 18]       # Valid for poly_mod_degree 4096 [cite: 147]
#         ]
        
#         return list(itertools.product(poly_mod_degrees, coeff_mod_combinations))

#encryption_manager.py new 3after 2nd

import tenseal as ts
from time import time
import torch
import itertools

class EncryptionManager:
    """Manages encryption operations and context."""
    
    def __init__(self):
        self.ctx_eval = None
        
    def generate_keys(self, poly_mod_degree=4096, coeff_mod_bit_sizes=None):
        """
        Generate encryption keys with configurable parameters.
        
        Args:
            poly_mod_degree (int): Polynomial modulus degree
            coeff_mod_bit_sizes (list): Coefficient modulus bit sizes
        """
        if coeff_mod_bit_sizes is None:
            coeff_mod_bit_sizes = [40, 20, 40]
        
        # Validate parameters based on TenSEAL library insights
        if poly_mod_degree not in [4096, 8192]:
            raise ValueError("Poly mod degree must be 4096 or 8192")
        
        if len(coeff_mod_bit_sizes) < 2 or any(size > 60 for size in coeff_mod_bit_sizes):
            raise ValueError("Invalid coefficient modulus. Each prime must be ≤ 60 bits")
        
        self.ctx_eval = ts.context(ts.SCHEME_TYPE.CKKS, poly_mod_degree, -1, coeff_mod_bit_sizes)
        self.ctx_eval.global_scale = 2 ** 20
        self.ctx_eval.generate_galois_keys()
        
    def encrypt_data(self, x_test):
        """
        Encrypt test data.
        
        Args:
            x_test (torch.Tensor): Test data to encrypt
            
        Returns:
            list: Encrypted test data
        """
        if self.ctx_eval is None:
            raise Exception("Keys not generated")

        if not isinstance(x_test, torch.Tensor):
            raise TypeError("Input must be a torch.Tensor")

        if x_test.numel() == 0:
            raise ValueError("Input tensor is empty")
        
        t_start = time()

        if x_test.ndimension() == 1:
            enc_x_test = [ts.ckks_vector(self.ctx_eval, x.tolist()) for x in x_test]
        elif x_test.ndimension() == 2:
            enc_x_test = [ts.ckks_vector(self.ctx_eval, row.tolist()) for row in x_test]
        else:
            raise ValueError("Only 1D and 2D tensors are supported for encryption")
        
        t_end = time()
        print(f"Encryption of the test-set took {int(t_end - t_start)} seconds")
        
        return enc_x_test

    def evaluate_model(self, model, enc_x_test, y_test):
        """
        Evaluate encrypted model performance.
        
        Args:
            model (EncryptedLR): Encrypted model
            enc_x_test (list): Encrypted test data
            y_test (torch.Tensor): Test targets
            
        Returns:
            float: Accuracy score
        """
        correct = 0
        for enc_x, y in zip(enc_x_test, y_test):
            enc_out = model(enc_x)
            out = enc_out.decrypt()
            out = torch.tensor(out)
            out = torch.sigmoid(out)
            if torch.abs(out - y) < 0.5:
                correct += 1
        return correct / len(y_test)
    
    @staticmethod
    def get_parameter_combinations():
        """
        Generate a list of parameter combinations to test.
        
        Returns:
            list: List of parameter combinations
        """
        poly_mod_degrees = [4096, 8192]
        coeff_mod_combinations = [
            [40, 20, 40]
        ]
        
        return list(itertools.product(poly_mod_degrees, coeff_mod_combinations))