import { useState } from "react";
import axios from "axios";

function UploadCSV() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Handle file selection
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setMessage("");
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a CSV file first.");
      return;
    }

    setIsLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      // const response = await axios.post("http://localhost:5000/upload", formData, {
      //   headers: { "Content-Type": "multipart/form-data" },
      // });

      const apiUrl = process.env.REACT_APP_API_URL;//for docker deploy with env
      const response = await axios.post(`${apiUrl}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data.error || "Error uploading file.");
      console.error("Upload Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Upload CSV File</h2>
      <p>Upload your dataset to begin the homomorphic encryption workflow.</p>
      <h1>Click the link to download a test file</h1>
      <a 
        href="https://drive.google.com/uc?export=download&id=132nRbq9PBuERDnFe4N6ZS7nxGSgk2fXU" 
        download="framingham.csv"
        target="_blank" 
        rel="noopener noreferrer"
      >
        Download Test Dataset
      </a>      
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={isLoading}>
        {isLoading ? "Uploading..." : "Upload"}
      </button>
      
      {isLoading && (
        <div className="progress-container">
          <div className="progress-bar active"></div>
        </div>
      )}
      
      {message && <p className={`message ${message.includes("Error") || message.includes("Please") ? "error" : "success"}`}>{message}</p>}
    </div>
  );
}

export default UploadCSV;