from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import random
import torch

from services.data_service import DataService
from services.model_service import ModelService
from services.encryption_service import EncryptionService
from services.analysis_service import AnalysisService

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

# Services
data_service = DataService()
model_service = ModelService()
encryption_service = EncryptionService()
analysis_service = AnalysisService(data_service, model_service, encryption_service)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():    
    return jsonify({"message": "Backend is running!"})

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload endpoint."""    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        data_service.set_file_path(filepath)
        return jsonify({"message": "File uploaded successfully!"}), 200
    
    return jsonify({"error": "Invalid file type!"}), 400

@app.route("/parameters", methods=["GET"])
def get_parameters():
    """Get available encryption parameters."""
    
    try:
        parameters = encryption_service.get_parameter_combinations()

        return jsonify({"parameters": [
            {"poly_mod_degree": p[0], "coeff_mod_bit_sizes": p[1]} 
            for p in parameters
        ]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/set-parameters", methods=["POST"])
def set_parameters():
    """Set encryption parameters."""    
    if not request.json:
        return jsonify({"error": "No parameters provided,"}), 400
        
    try:        
        print("Received data:", request.json)  # Add this line
        
        poly_mod_degree = request.json.get('poly_mod_degree', 4096)
        coeff_mod_bit_sizes = request.json.get('coeff_mod_bit_sizes', [40, 20, 40])
                
        #Set user parameters inside encryption_service
        encryption_service.set_user_selected_parameters(poly_mod_degree, coeff_mod_bit_sizes)                
        
        encryption_service.generate_keys(poly_mod_degree, coeff_mod_bit_sizes)        
        
        return jsonify({
            "message": "Parameters set successfully",
            "poly_mod_degree": poly_mod_degree,
            "coeff_mod_bit_sizes": coeff_mod_bit_sizes
        }), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate-keys", methods=["GET"])
def generate_keys():
    """Generate keys and analyze parameter impact on performance."""    
    if not data_service.has_file():
        return jsonify({"error": "Please upload dataset first!!"}), 400
        
    try:
        # Process data and train model only once        
        data_service.process_data()
        
        model_service.train_model(data_service.get_training_data())
        
        # Perform parameter analysis        
        results = analysis_service.analyze_parameters()        
        
        return jsonify({"results": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/encrypt", methods=["POST"])
def encrypt():
    """Encrypt test data endpoint."""    
    if not data_service.has_file():
        return jsonify({"error": "Please upload dataset first!!"}), 400
        
    if not encryption_service.has_context():
        return jsonify({"error": "Please generate keys first!!"}), 400
    
    params = request.json or {}
    poly_mod_degree = params.get('poly_mod_degree', 4096)
    coeff_mod_bit_sizes = params.get('coeff_mod_bit_sizes', [40, 20, 40])
        
    try:
        # Generate keys with specified parameters if they weren't set already
        if not encryption_service.has_context():            
            encryption_service.generate_keys(poly_mod_degree, coeff_mod_bit_sizes)
            
        # Encrypt the test data        
        encryption_service.encrypt_data(data_service.get_test_features())        
        
        return jsonify({"message": "Data encrypted successfully!!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/compute", methods=["GET"])
def compute():
    """Compute accuracy results with encrypted data."""    
    if not data_service.has_file():
        return jsonify({"error": "Please upload dataset first!!"}), 400
            
    if not encryption_service.has_context():
        return jsonify({"error": "Please generate keys first!!"}), 400
        
    if not encryption_service.has_encrypted_data():
        return jsonify({"error": "Please encrypt data first!!"}), 400

    try:
        # Create encrypted model from trained model        
        model_service.create_encrypted_model()
        
        # Calculate plain accuracy
        plain_metrics = model_service.evaluate_plain_metrics(
            data_service.get_test_features(), 
            data_service.get_test_targets()
        )
        
        # Calculate encrypted accuracy        
        encrypted_metrics = encryption_service.encrypted_evaluation(
            model_service.get_encrypted_model(),
            encryption_service.get_encrypted_data(),
            data_service.get_test_targets()
        )
        
        diff_metrics = {}
        for metric in ['accuracy', 'precision', 'recall', 'f1']:
            diff = plain_metrics[metric] - encrypted_metrics[metric]
            diff_metrics[metric] = round(diff, 4)
                
        
        # Compute differences for each metric        
        response_data = {
            "message": "Computation completed successfully",
            "plain_metrics": plain_metrics,
            "encrypted_metrics": encrypted_metrics,
            "difference_metrics": diff_metrics
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        print(f"Error in /compute: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/download-results", methods=["GET"])
def download_results():
    """Prepare analysis results for download with optional filtering."""    
    if not data_service.has_file():
        return jsonify({"error": "Please upload dataset first!!"}), 400
    
    filter_type = request.args.get('filter', 'all')

    try:
        # Generate fresh analysis if needed
        if not analysis_service.has_results():
            
            data_service.process_data()
            
            model_service.train_model(data_service.get_training_data())
            
            analysis_service.analyze_parameters()        
        
        results = analysis_service.get_results()

        # Filter results if requested
        selected_params = encryption_service.get_user_selected_parameters()
        if filter_type == 'selected' and selected_params:
            
            filtered_results = [r for r in results if 
                r["poly_mod_degree"] == selected_params["poly_mod_degree"] and 
                r["coeff_mod_bit_sizes"] == selected_params["coeff_mod_bit_sizes"]]
            return jsonify({"results": filtered_results}), 200
        
        return jsonify({"results": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":    
    app.run(debug=True)  # False for production to handle multiple requests

