#before updating3-26-25
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from werkzeug.utils import secure_filename
# import torch
# import random

# from data_handler import process_heart_disease_data
# from model_manager import LR, EncryptedLR, train_model
# from encryption_manager import EncryptionManager

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # App configuration
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'csv'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Create uploads directory
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Set random seeds
# torch.random.manual_seed(73)
# random.seed(73)

# # Global state
# uploaded_file_path = None
# x_test = None
# y_test = None
# model = None
# encryption_manager = EncryptionManager()
# enc_x_test = None

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route("/")
# def home():
#     return jsonify({"message": "Backend is running!1"})

# @app.route("/upload", methods=["POST"])
# def upload_file():
#     """Handle file upload endpoint."""
#     global uploaded_file_path
    
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part2"}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file3"}), 400
    
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
#         uploaded_file_path = filepath
#         return jsonify({"message": "File uploaded successfully!!4"}), 200
    
#     return jsonify({"error": "Invalid file type!!5"}), 400

# @app.route("/generate-keys", methods=["GET"])
# def generate_keys():
#     """Generate keys and train model endpoint."""
#     global model, x_test, y_test
    
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     try:
#         # Process data 
#         x_train, y_train, x_test, y_test = process_heart_disease_data(uploaded_file_path)
        
#         # Train model
#         model = LR(x_train.shape[1])
#         model = train_model(model, x_train, y_train)
        
#         # Generate encryption keys
#         encryption_manager.generate_keys()

#         return jsonify({"message": "Keys generated and model trained successfully!!"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/encrypt", methods=["POST"])
# def encrypt():
#     """Encrypt test data endpoint."""
#     global enc_x_test
    
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     if encryption_manager.ctx_eval is None:
#         return jsonify({"error": "Please generate keys first!!"}), 400
        
#     try:
#         enc_x_test = encryption_manager.encrypt_data(x_test)
#         return jsonify({"message": "Data encrypted successfully!!"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/compute", methods=["GET"])
# def compute():
#     """Compute results endpoint."""
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     if encryption_manager.ctx_eval is None:
#         return jsonify({"error": "Please generate keys first!!"}), 400
        
#     if enc_x_test is None:
#         return jsonify({"error": "Please encrypt data first!!"}), 400

#     try:
#         # Create encrypted model
#         eelr = EncryptedLR(model)
        
#         # Calculate plain accuracy
#         def accuracy(model, x, y):
#             out = model(x)
#             correct = torch.abs(y - out) < 0.5
#             return correct.float().mean()
            
#         plain_accuracy = accuracy(model, x_test, y_test)
        
#         # Calculate encrypted accuracy
#         encrypted_accuracy = encryption_manager.evaluate_model(eelr, enc_x_test, y_test)
#         diff_accuracy = plain_accuracy - encrypted_accuracy
        
#         response_data = {
#             "message": "Computation completed successfully",
#             "encrypted_accuracy": float(encrypted_accuracy),
#             "plain_accuracy": float(plain_accuracy),
#             "diff_accuracy": float(diff_accuracy)
#         }
        
#         return jsonify(response_data), 200
        
#     except Exception as e:
#         print(f"Error in /compute: {str(e)}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)

# # updated one 3-26-25 new 1
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from werkzeug.utils import secure_filename
# import torch
# import random
# from time import time


# from data_handler import process_heart_disease_data
# from model_manager import LR, EncryptedLR, train_model
# from encryption_manager import EncryptionManager

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # App configuration
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'csv'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Create uploads directory
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Set random seeds
# torch.random.manual_seed(73)
# random.seed(73)

# # Global state
# uploaded_file_path = None
# x_test = None
# y_test = None
# model = None
# encryption_manager = EncryptionManager()
# enc_x_test = None

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route("/")
# def home():
#     return jsonify({"message": "Backend is running!1"})

# @app.route("/upload", methods=["POST"])
# def upload_file():
#     """Handle file upload endpoint."""
#     global uploaded_file_path
    
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part2"}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file3"}), 400
    
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
#         uploaded_file_path = filepath
#         return jsonify({"message": "File uploaded successfully!!4"}), 200
    
#     return jsonify({"error": "Invalid file type!!5"}), 400

# @app.route("/generate-keys", methods=["GET"])
# def generate_keys():
#     """Generate keys and train model endpoint with parameter analysis."""
#     global model, x_test, y_test
    
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     try:
#         # Process data 
#         x_train, y_train, x_test, y_test = process_heart_disease_data(uploaded_file_path)
        
#         # Perform parameter analysis
#         results = []
        
#         # Get parameter combinations
#         param_combinations = encryption_manager.get_parameter_combinations()
        
#         for poly_mod_degree, coeff_mod_bit_sizes in param_combinations:
#             # Reset model for each parameter set
#             model = LR(x_train.shape[1])
            
#             # Train model
#             start_train_time = time()
#             model = train_model(model, x_train, y_train)
#             train_time = time() - start_train_time
            
#             # Generate keys with specific parameters
#             start_key_gen_time = time()
#             encryption_manager.generate_keys(
#                 poly_mod_degree=poly_mod_degree, 
#                 coeff_mod_bit_sizes=coeff_mod_bit_sizes
#             )
#             key_gen_time = time() - start_key_gen_time
            
#             # Encrypt test data
#             start_encrypt_time = time()
#             enc_x_test = encryption_manager.encrypt_data(x_test)
#             encrypt_time = time() - start_encrypt_time
            
#             # Create encrypted model
#             eelr = EncryptedLR(model)
            
#             # Calculate plain accuracy
#             def accuracy(model, x, y):
#                 out = model(x)
#                 correct = torch.abs(y - out) < 0.5
#                 return correct.float().mean()
            
#             plain_accuracy = accuracy(model, x_test, y_test)
            
#             # Calculate encrypted accuracy
#             start_compute_time = time()
#             encrypted_accuracy = encryption_manager.evaluate_model(eelr, enc_x_test, y_test)
#             compute_time = time() - start_compute_time
            
#             # Store results
#             results.append({
#                 "poly_mod_degree": poly_mod_degree,
#                 "coeff_mod_bit_sizes": coeff_mod_bit_sizes,
#                 "train_time": train_time,
#                 "key_gen_time": key_gen_time,
#                 "encrypt_time": encrypt_time,
#                 "compute_time": compute_time,
#                 "plain_accuracy": float(plain_accuracy),
#                 "encrypted_accuracy": float(encrypted_accuracy)
#             })
        
#         return jsonify({"results": results}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/encrypt", methods=["POST"])
# def encrypt():
#     """Encrypt test data endpoint."""
#     global enc_x_test
    
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     if encryption_manager.ctx_eval is None:
#         return jsonify({"error": "Please generate keys first!!"}), 400
        
#     try:
#         enc_x_test = encryption_manager.encrypt_data(x_test)
#         return jsonify({"message": "Data encrypted successfully!!"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/compute", methods=["GET"])
# def compute():
#     """Compute results endpoint."""
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     if encryption_manager.ctx_eval is None:
#         return jsonify({"error": "Please generate keys first!!"}), 400
        
#     if enc_x_test is None:
#         return jsonify({"error": "Please encrypt data first!!"}), 400

#     try:
#         # Create encrypted model
#         eelr = EncryptedLR(model)
        
#         # Calculate plain accuracy
#         def accuracy(model, x, y):
#             out = model(x)
#             correct = torch.abs(y - out) < 0.5
#             return correct.float().mean()
            
#         plain_accuracy = accuracy(model, x_test, y_test)
        
#         # Calculate encrypted accuracy
#         encrypted_accuracy = encryption_manager.evaluate_model(eelr, enc_x_test, y_test)
#         diff_accuracy = plain_accuracy - encrypted_accuracy
        
#         response_data = {
#             "message": "Computation completed successfully",
#             "encrypted_accuracy": float(encrypted_accuracy),
#             "plain_accuracy": float(plain_accuracy),
#             "diff_accuracy": float(diff_accuracy)
#         }
        
#         return jsonify(response_data), 200
        
#     except Exception as e:
#         print(f"Error in /compute: {str(e)}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)

# #3-26-25 new 2

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from werkzeug.utils import secure_filename
# import torch
# import random
# from time import time

# from data_handler import process_heart_disease_data
# from model_manager import LR, EncryptedLR, train_model
# from encryption_manager import EncryptionManager

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # App configuration
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'csv'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Create uploads directory
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Set random seeds
# torch.random.manual_seed(73)
# random.seed(73)

# # Global state
# uploaded_file_path = None
# x_test = None
# y_test = None
# model = None
# encryption_manager = EncryptionManager()

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route("/")
# def home():
#     return jsonify({"message": "Backend is running!"})

# @app.route("/upload", methods=["POST"])
# def upload_file():
#     """Handle file upload endpoint."""
#     global uploaded_file_path
    
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
    
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
#         uploaded_file_path = filepath
#         return jsonify({"message": "File uploaded successfully!"}), 200
    
#     return jsonify({"error": "Invalid file type!"}), 400

# @app.route("/generate-keys", methods=["GET"])
# def generate_keys():
#     """Generate keys and train model endpoint with parameter analysis."""
#     global model, x_test, y_test
    
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     try:
#         # Process data 
#         x_train, y_train, x_test, y_test = process_heart_disease_data(uploaded_file_path)
        
#         # Perform parameter analysis
#         results = []
        
#         # Get parameter combinations
#         param_combinations = encryption_manager.get_parameter_combinations()
        
#         for poly_mod_degree, coeff_mod_bit_sizes in param_combinations:
#             try:
#                 print(f"Trying poly_mod_degree={poly_mod_degree}, coeff_mod_bit_sizes={coeff_mod_bit_sizes}")
#                 # Reset model for each parameter set
#                 model = LR(x_train.shape[1])
                
#                 # Train model
#                 start_train_time = time()
#                 model = train_model(model, x_train, y_train)
#                 train_time = time() - start_train_time
                
#                 # Generate keys with specific parameters
#                 start_key_gen_time = time()
#                 encryption_manager.generate_keys(
#                     poly_mod_degree=poly_mod_degree, 
#                     coeff_mod_bit_sizes=coeff_mod_bit_sizes
#                 )
#                 key_gen_time = time() - start_key_gen_time
                
#             except ValueError as ve:
#                 print(f"Parameter error: {ve}")
#                 continue
#             # # Reset model for each parameter set
#             # model = LR(x_train.shape[1])
            
#             # # Train model
#             # start_train_time = time()
#             # model = train_model(model, x_train, y_train)
#             # train_time = time() - start_train_time
            
#             # # Generate keys with specific parameters
#             # start_key_gen_time = time()
#             # encryption_manager.generate_keys(
#             #     poly_mod_degree=poly_mod_degree, 
#             #     coeff_mod_bit_sizes=coeff_mod_bit_sizes
#             # )
#             # key_gen_time = time() - start_key_gen_time
            
#             # Encrypt test data
#             start_encrypt_time = time()
#             enc_x_test = encryption_manager.encrypt_data(x_test)
#             encrypt_time = time() - start_encrypt_time
            
#             # Create encrypted model
#             eelr = EncryptedLR(model)
            
#             # Calculate plain accuracy
#             def accuracy(model, x, y):
#                 out = model(x)
#                 correct = torch.abs(y - out) < 0.5
#                 return correct.float().mean()
            
#             plain_accuracy = accuracy(model, x_test, y_test)
            
#             # Calculate encrypted accuracy
#             start_compute_time = time()
#             encrypted_accuracy = encryption_manager.evaluate_model(eelr, enc_x_test, y_test)
#             compute_time = time() - start_compute_time
            
#             # Store results
#             results.append({
#                 "poly_mod_degree": poly_mod_degree,
#                 "coeff_mod_bit_sizes": coeff_mod_bit_sizes,
#                 "train_time": train_time,
#                 "key_gen_time": key_gen_time,
#                 "encrypt_time": encrypt_time,
#                 "compute_time": compute_time,
#                 "plain_accuracy": float(plain_accuracy),
#                 "encrypted_accuracy": float(encrypted_accuracy)
#             })
        
#         return jsonify({"results": results}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/encrypt", methods=["POST"])
# def encrypt():
#     """Encrypt test data endpoint."""
#     global enc_x_test
    
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     if encryption_manager.ctx_eval is None:
#         return jsonify({"error": "Please generate keys first!!"}), 400
        
#     try:
#         enc_x_test = encryption_manager.encrypt_data(x_test)
#         return jsonify({"message": "Data encrypted successfully!!"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/compute", methods=["GET"])
# def compute():
#     """Compute results endpoint."""
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     if encryption_manager.ctx_eval is None:
#         return jsonify({"error": "Please generate keys first!!"}), 400
        
#     if enc_x_test is None:
#         return jsonify({"error": "Please encrypt data first!!"}), 400

#     try:
#         # Create encrypted model
#         eelr = EncryptedLR(model)
        
#         # Calculate plain accuracy
#         def accuracy(model, x, y):
#             out = model(x)
#             correct = torch.abs(y - out) < 0.5
#             return correct.float().mean()
            
#         plain_accuracy = accuracy(model, x_test, y_test)
        
#         # Calculate encrypted accuracy
#         encrypted_accuracy = encryption_manager.evaluate_model(eelr, enc_x_test, y_test)
#         diff_accuracy = plain_accuracy - encrypted_accuracy
        
#         response_data = {
#             "message": "Computation completed successfully",
#             "encrypted_accuracy": float(encrypted_accuracy),
#             "plain_accuracy": float(plain_accuracy),
#             "diff_accuracy": float(diff_accuracy)
#         }
        
#         return jsonify(response_data), 200
        
#     except Exception as e:
#         print(f"Error in /compute: {str(e)}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)

# #back to new 1 with a error handiling massage effect 2 files
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from werkzeug.utils import secure_filename
# import torch
# import random
# from time import time

# from data_handler import process_heart_disease_data
# from model_manager import LR, EncryptedLR, train_model
# from encryption_manager import EncryptionManager

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # App configuration
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'csv'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Create uploads directory
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Set random seeds
# torch.random.manual_seed(73)
# random.seed(73)

# # Global state
# uploaded_file_path = None
# x_test = None
# y_test = None
# model = None
# encryption_manager = EncryptionManager()

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route("/")
# def home():
#     return jsonify({"message": "Backend is running!"})

# @app.route("/upload", methods=["POST"])
# def upload_file():
#     """Handle file upload endpoint."""
#     global uploaded_file_path
    
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
    
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
#         uploaded_file_path = filepath
#         return jsonify({"message": "File uploaded successfully!"}), 200
    
#     return jsonify({"error": "Invalid file type!"}), 400

# @app.route("/generate-keys", methods=["GET"])
# def generate_keys():
#     """Generate keys and train model endpoint with parameter analysis."""
#     global model, x_test, y_test
    
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     try:
#         # Process data 
#         x_train, y_train, x_test, y_test = process_heart_disease_data(uploaded_file_path)
        
#         # Perform parameter analysis
#         results = []
        
#         # Get parameter combinations
#         param_combinations = encryption_manager.get_parameter_combinations()
        
#         for poly_mod_degree, coeff_mod_bit_sizes in param_combinations:
#             print(f"Trying poly_mod_degree={poly_mod_degree}, coeff_mod_bit_sizes={coeff_mod_bit_sizes}")#new error print added
#             # Reset model for each parameter set
#             model = LR(x_train.shape[1])
            
#             # Train model
#             start_train_time = time()
#             model = train_model(model, x_train, y_train)
#             train_time = time() - start_train_time
            
#             # Generate keys with specific parameters
#             start_key_gen_time = time()
#             encryption_manager.generate_keys(
#                 poly_mod_degree=poly_mod_degree, 
#                 coeff_mod_bit_sizes=coeff_mod_bit_sizes
#             )
#             key_gen_time = time() - start_key_gen_time
            
#             # Encrypt test data
#             start_encrypt_time = time()
#             enc_x_test = encryption_manager.encrypt_data(x_test)
#             encrypt_time = time() - start_encrypt_time
            
#             # Create encrypted model
#             eelr = EncryptedLR(model)
            
#             # Calculate plain accuracy
#             def accuracy(model, x, y):
#                 out = model(x)
#                 correct = torch.abs(y - out) < 0.5
#                 return correct.float().mean()
            
#             plain_accuracy = accuracy(model, x_test, y_test)
            
#             # Calculate encrypted accuracy
#             start_compute_time = time()
#             encrypted_accuracy = encryption_manager.evaluate_model(eelr, enc_x_test, y_test)
#             compute_time = time() - start_compute_time
            
#             # Store results
#             results.append({
#                 "poly_mod_degree": poly_mod_degree,
#                 "coeff_mod_bit_sizes": coeff_mod_bit_sizes,
#                 "train_time": train_time,
#                 "key_gen_time": key_gen_time,
#                 "encrypt_time": encrypt_time,
#                 "compute_time": compute_time,
#                 "plain_accuracy": float(plain_accuracy),
#                 "encrypted_accuracy": float(encrypted_accuracy)
#             })
        
#         return jsonify({"results": results}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/encrypt", methods=["POST"])
# def encrypt():
#     """Encrypt test data endpoint."""
#     global enc_x_test
    
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     if encryption_manager.ctx_eval is None:
#         return jsonify({"error": "Please generate keys first!!"}), 400
        
#     try:
#         enc_x_test = encryption_manager.encrypt_data(x_test)
#         return jsonify({"message": "Data encrypted successfully!!"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/compute", methods=["GET"])
# def compute():
#     """Compute results endpoint."""
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     if encryption_manager.ctx_eval is None:
#         return jsonify({"error": "Please generate keys first!!"}), 400
        
#     if enc_x_test is None:
#         return jsonify({"error": "Please encrypt data first!!"}), 400

#     try:
#         # Create encrypted model
#         eelr = EncryptedLR(model)
        
#         # Calculate plain accuracy
#         def accuracy(model, x, y):
#             out = model(x)
#             correct = torch.abs(y - out) < 0.5
#             return correct.float().mean()
            
#         plain_accuracy = accuracy(model, x_test, y_test)
        
#         # Calculate encrypted accuracy
#         encrypted_accuracy = encryption_manager.evaluate_model(eelr, enc_x_test, y_test)
#         diff_accuracy = plain_accuracy - encrypted_accuracy
        
#         response_data = {
#             "message": "Computation completed successfully",
#             "encrypted_accuracy": float(encrypted_accuracy),
#             "plain_accuracy": float(plain_accuracy),
#             "diff_accuracy": float(diff_accuracy)
#         }
        
#         return jsonify(response_data), 200
        
#     except Exception as e:
#         print(f"Error in /compute: {str(e)}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)


#app.py new 3 came back

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import torch
import random
from time import time

from data_handler import process_heart_disease_data
from model_manager import LR, EncryptedLR, train_model
from encryption_manager import EncryptionManager

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# App configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set random seeds
torch.random.manual_seed(73)
random.seed(73)

# Global state
uploaded_file_path = None
x_test = None
y_test = None
model = None
encryption_manager = EncryptionManager()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"})

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload endpoint."""
    global uploaded_file_path
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        uploaded_file_path = filepath
        return jsonify({"message": "File uploaded successfully!"}), 200
    
    return jsonify({"error": "Invalid file type!"}), 400

@app.route("/generate-keys", methods=["GET"])
def generate_keys():
    """Generate keys and train model endpoint with parameter analysis."""
    global model, x_test, y_test
    
    if uploaded_file_path is None:
        return jsonify({"error": "Please upload dataset first!!"}), 400
        
    try:
        # Process data 
        x_train, y_train, x_test, y_test = process_heart_disease_data(uploaded_file_path)
        
        # Perform parameter analysis
        results = []
        
        # Get parameter combinations
        param_combinations = encryption_manager.get_parameter_combinations()
        
        for poly_mod_degree, coeff_mod_bit_sizes in param_combinations:
            try:
                print(f"Trying poly_mod_degree={poly_mod_degree}, coeff_mod_bit_sizes={coeff_mod_bit_sizes}")
                
                # Reset model for each parameter set
                model = LR(x_train.shape[1])
                
                # Train model and measure time
                start_train_time = time()
                model = train_model(model, x_train, y_train)
                train_time = time() - start_train_time
                
                # Generate keys with specific parameters and measure time
                start_key_gen_time = time()
                encryption_manager.generate_keys(
                    poly_mod_degree=poly_mod_degree, 
                    coeff_mod_bit_sizes=coeff_mod_bit_sizes
                )
                key_gen_time = time() - start_key_gen_time
                
                # Encrypt test data and measure time
                start_encrypt_time = time()
                enc_x_test = encryption_manager.encrypt_data(x_test)
                encrypt_time = time() - start_encrypt_time
                
                # Create encrypted model
                eelr = EncryptedLR(model)
                
                # Calculate plain accuracy and measure time
                start_plain_compute_time = time()
                def accuracy(model, x, y):
                    out = model(x)
                    correct = torch.abs(y - out) < 0.5
                    return correct.float().mean()
                
                plain_accuracy = accuracy(model, x_test, y_test)
                plain_compute_time = time() - start_plain_compute_time
                
                # Calculate encrypted accuracy and measure time
                start_encrypted_compute_time = time()
                encrypted_accuracy = encryption_manager.evaluate_model(eelr, enc_x_test, y_test)
                encrypted_compute_time = time() - start_encrypted_compute_time
                
                # Store results
                results.append({
                    "poly_mod_degree": poly_mod_degree,
                    "coeff_mod_bit_sizes": coeff_mod_bit_sizes,
                    "train_time": train_time,
                    "key_gen_time": key_gen_time,
                    "encrypt_time": encrypt_time,
                    "plain_compute_time": plain_compute_time,
                    "encrypted_compute_time": encrypted_compute_time,
                    "plain_accuracy": float(plain_accuracy),
                    "encrypted_accuracy": float(encrypted_accuracy)
                })
                
            except ValueError as ve:
                print(f"Parameter error: {ve}")
                continue
        
        return jsonify({"results": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Other routes remain the same (encrypt, compute, etc.)
@app.route("/encrypt", methods=["POST"])
def encrypt():
    """Encrypt test data endpoint."""
    global enc_x_test
    
    if uploaded_file_path is None:
        return jsonify({"error": "Please upload dataset first!!"}), 400
        
    if encryption_manager.ctx_eval is None:
        return jsonify({"error": "Please generate keys first!!"}), 400
        
    try:
        enc_x_test = encryption_manager.encrypt_data(x_test)
        return jsonify({"message": "Data encrypted successfully!!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/compute", methods=["GET"])
def compute():
    """Compute results endpoint."""
    if uploaded_file_path is None:
        return jsonify({"error": "Please upload dataset first!!"}), 400
        
    if encryption_manager.ctx_eval is None:
        return jsonify({"error": "Please generate keys first!!"}), 400
        
    if enc_x_test is None:
        return jsonify({"error": "Please encrypt data first!!"}), 400

    try:
        # Create encrypted model
        eelr = EncryptedLR(model)
        
        # Calculate plain accuracy
        def accuracy(model, x, y):
            out = model(x)
            correct = torch.abs(y - out) < 0.5
            return correct.float().mean()
            
        plain_accuracy = accuracy(model, x_test, y_test)
        
        # Calculate encrypted accuracy
        encrypted_accuracy = encryption_manager.evaluate_model(eelr, enc_x_test, y_test)
        diff_accuracy = plain_accuracy - encrypted_accuracy
        
        response_data = {
            "message": "Computation completed successfully",
            "encrypted_accuracy": float(encrypted_accuracy),
            "plain_accuracy": float(plain_accuracy),
            "diff_accuracy": float(diff_accuracy)
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"Error in /compute: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)



# #app.py new 4 3 files for 2 idea

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# from werkzeug.utils import secure_filename
# import torch
# import random
# from time import time

# from data_handler import process_heart_disease_data
# from model_manager import LR, EncryptedLR, train_model
# from encryption_manager import EncryptionManager

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # App configuration
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'csv'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Create uploads directory
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# # Set random seeds
# torch.random.manual_seed(73)
# random.seed(73)

# # Global state
# uploaded_file_path = None
# x_test = None
# y_test = None
# model = None
# encryption_manager = EncryptionManager()

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route("/")
# def home():
#     return jsonify({"message": "Backend is running!"})

# @app.route("/upload", methods=["POST"])
# def upload_file():
#     """Handle file upload endpoint."""
#     global uploaded_file_path
    
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
    
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
#         uploaded_file_path = filepath
#         return jsonify({"message": "File uploaded successfully!"}), 200
    
#     return jsonify({"error": "Invalid file type!"}), 400

# @app.route("/generate-keys", methods=["GET"])
# def generate_keys():
#     """Generate keys and train model endpoint with parameter analysis."""
#     global model, x_test, y_test
    
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     try:
#         # Process data 
#         x_train, y_train, x_test, y_test = process_heart_disease_data(uploaded_file_path)
        
#         # Perform parameter analysis
#         results = []
        
#         # Get parameter combinations
#         param_combinations = encryption_manager.get_parameter_combinations()
        
#         for poly_mod_degree, coeff_mod_bit_sizes in param_combinations:
#             try:
#                 print(f"Trying poly_mod_degree={poly_mod_degree}, coeff_mod_bit_sizes={coeff_mod_bit_sizes}")
                
#                 # Reset model for each parameter set
#                 model = LR(x_train.shape[1])
                
#                 # Train model and measure time
#                 start_train_time = time()
#                 model = train_model(model, x_train, y_train)
#                 train_time = time() - start_train_time
                
#                 # Generate keys with specific parameters and measure time
#                 start_key_gen_time = time()
#                 encryption_manager.generate_keys(
#                     poly_mod_degree=poly_mod_degree, 
#                     coeff_mod_bit_sizes=coeff_mod_bit_sizes
#                 )
#                 key_gen_time = time() - start_key_gen_time
                
#                 # Encrypt test data and measure time
#                 start_encrypt_time = time()
#                 enc_x_test = encryption_manager.encrypt_data(x_test)
#                 encrypt_time = time() - start_encrypt_time
                
#                 # Create encrypted model
#                 eelr = EncryptedLR(model)
                
#                 # Calculate plain accuracy and measure time
#                 start_plain_compute_time = time()
#                 def accuracy(model, x, y):
#                     out = model(x)
#                     correct = torch.abs(y - out) < 0.5
#                     return correct.float().mean()
                
#                 plain_accuracy = accuracy(model, x_test, y_test)
#                 plain_compute_time = time() - start_plain_compute_time
                
#                 # Calculate encrypted accuracy and measure time
#                 start_encrypted_compute_time = time()
#                 encrypted_accuracy = encryption_manager.evaluate_model(eelr, enc_x_test, y_test)
#                 encrypted_compute_time = time() - start_encrypted_compute_time
                
#                 # Store results
#                 results.append({
#                     "poly_mod_degree": poly_mod_degree,
#                     "coeff_mod_bit_sizes": coeff_mod_bit_sizes,
#                     "train_time": train_time,
#                     "key_gen_time": key_gen_time,
#                     "encrypt_time": encrypt_time,
#                     "plain_compute_time": plain_compute_time,
#                     "encrypted_compute_time": encrypted_compute_time,
#                     "plain_accuracy": float(plain_accuracy),
#                     "encrypted_accuracy": float(encrypted_accuracy)
#                 })
                
#             except ValueError as ve:
#                 print(f"Parameter error: {ve}")
#                 continue
        
#         return jsonify({"results": results}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Other routes remain the same (encrypt, compute, etc.)
# @app.route("/encrypt", methods=["POST"])
# def encrypt():
#     """Encrypt test data endpoint."""
#     global enc_x_test
    
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     if encryption_manager.ctx_eval is None:
#         return jsonify({"error": "Please generate keys first!!"}), 400
        
#     try:
#         enc_x_test = encryption_manager.encrypt_data(x_test)
#         return jsonify({"message": "Data encrypted successfully!!"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route("/compute", methods=["GET"])
# def compute():
#     """Compute results endpoint with noise analysis."""
#     if uploaded_file_path is None:
#         return jsonify({"error": "Please upload dataset first!!"}), 400
        
#     if encryption_manager.ctx_eval is None:
#         return jsonify({"error": "Please generate keys first!!"}), 400
        
#     if enc_x_test is None:
#         return jsonify({"error": "Please encrypt data first!!"}), 400

#     try:
#         # Create encrypted model
#         eelr = EncryptedLR(model)
        
#         # Calculate plain accuracy and outputs
#         def accuracy_and_outputs(model, x, y):
#             out = model(x)
#             correct = torch.abs(y - out) < 0.5
#             return correct.float().mean(), out
            
#         plain_accuracy, plain_outputs = accuracy_and_outputs(model, x_test, y_test)
        
#         # Calculate encrypted accuracy and outputs
#         encrypted_outputs = []
#         for enc_x, y in zip(enc_x_test, y_test):
#             enc_out = model(enc_x)
#             encrypted_outputs.append(torch.tensor(enc_out.decrypt()))
        
#         encrypted_outputs = torch.stack(encrypted_outputs)
#         encrypted_outputs = torch.sigmoid(encrypted_outputs)
        
#         # Calculate accuracies
#         encrypted_accuracy = (torch.abs(encrypted_outputs - y_test) < 0.5).float().mean()
#         diff_accuracy = plain_accuracy - encrypted_accuracy
        
#         # Calculate noise metrics
#         noise_variance = torch.var(encrypted_outputs - plain_outputs)
#         noise_std_dev = torch.std(encrypted_outputs - plain_outputs)
        
#         response_data = {
#             "message": "Computation completed successfully",
#             "encrypted_accuracy": float(encrypted_accuracy),
#             "plain_accuracy": float(plain_accuracy),
#             "diff_accuracy": float(diff_accuracy),
#             "noise_variance": float(noise_variance),
#             "noise_std_dev": float(noise_std_dev)
#         }
        
#         return jsonify(response_data), 200
        
#     except Exception as e:
#         print(f"Error in /compute: {str(e)}")
#         return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     app.run(debug=True)

