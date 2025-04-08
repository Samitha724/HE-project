from time import time

class AnalysisService:
    """Service for analyzing encryption parameters and performance."""
    
    def __init__(self, data_service, model_service, encryption_service):
        self.data_service = data_service
        self.model_service = model_service
        self.encryption_service = encryption_service
        self.results = []
        
    def has_results(self):
        """Check if analysis results exist."""
        return len(self.results) > 0
        
    def get_results(self):
        """Get analysis results."""
        return self.results
        
    def analyze_parameters(self):
        """Analyze performance with different encryption parameters."""
        self.results = []
        
        # Get parameter combinations
        param_combinations = self.encryption_service.get_parameter_combinations()
        
        # Get trained model's plain accuracy (only compute once)
        x_test = self.data_service.get_test_features() 
        y_test = self.data_service.get_test_targets()
        
        # Record training time
        start_train_time = time()
        # model is already trained
        train_time = time() - start_train_time
                
        start_plain_compute_time = time()
        # Compute plain metrics once (they are not expected to change across parameter tests)
        plain_metrics = self.model_service.evaluate_plain_metrics(x_test, y_test)
        plain_compute_time = time() - start_plain_compute_time

        # Test each parameter combination
        for poly_mod_degree, coeff_mod_bit_sizes in param_combinations:
            try:
                print(f"Testing poly_mod_degree={poly_mod_degree}, coeff_mod_bit_sizes={coeff_mod_bit_sizes}")
                
                # Generate keys with the specific parameters
                start_key_gen_time = time()
                self.encryption_service.generate_keys(
                    poly_mod_degree=poly_mod_degree, 
                    coeff_mod_bit_sizes=coeff_mod_bit_sizes
                )
                key_gen_time = time() - start_key_gen_time
                
                # Encrypt test data
                start_encrypt_time = time()
                self.encryption_service.encrypt_data(x_test)
                encrypt_time = time() - start_encrypt_time
                
                # Create the Encrypted model 
                self.model_service.create_encrypted_model()                

                start_encrypted_compute_time = time()
                encrypted_metrics = self.encryption_service.encrypted_evaluation(
                    self.model_service.get_encrypted_model(),
                    self.encryption_service.get_encrypted_data(),
                    y_test
                )
                encrypted_compute_time = time() - start_encrypted_compute_time
                
                # Storing the results
                self.results.append({
                    "poly_mod_degree": poly_mod_degree,
                    "coeff_mod_bit_sizes": coeff_mod_bit_sizes,
                    "train_time": train_time,
                    "key_gen_time": key_gen_time,
                    "encrypt_time": encrypt_time,
                    "plain_compute_time": plain_compute_time,
                    "encrypted_compute_time": encrypted_compute_time,
                    "plain_accuracy": plain_metrics["accuracy"],
                    "plain_precision": plain_metrics["precision"],
                    "plain_recall": plain_metrics["recall"],
                    "plain_f1": plain_metrics["f1"],                    
                    "encrypted_accuracy": encrypted_metrics["accuracy"],
                    "encrypted_precision": encrypted_metrics["precision"],
                    "encrypted_recall": encrypted_metrics["recall"],
                    "encrypted_f1": encrypted_metrics["f1"]                    
                })
                
            except ValueError as ve:
                print(f"Parameter error: {ve}")
                continue
                
        return self.results