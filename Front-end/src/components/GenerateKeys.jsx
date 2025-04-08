import { useState } from "react";
import axios from "axios";

const GenerateKeys = () => {
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleGenerateKeys = async () => {
    setIsLoading(true);
    try {
      // const response = await axios.get("http://localhost:5000/generate-keys");

      const apiUrl = process.env.REACT_APP_API_URL;//for docker deploy with env
      const response = await axios.get(`${apiUrl}/generate-keys`);

      setMessage(response.data.message || "Keys generated successfully!");
    } catch (error) {
      setMessage(error.response?.data.error || "Error generating keys");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Generate Homomorphic Encryption Keys</h2>
      <p>Generate the necessary keys for encryption using the current parameters.</p>
      
      <button onClick={handleGenerateKeys} disabled={isLoading}>
        {isLoading ? "Generating..." : "Generate Keys"}
      </button>
      
      {isLoading && (
        <div className="progress-container">
          <div className="progress-bar active"></div>
        </div>
      )}
      
      {message && <p className={`message ${message.includes("Error") ? "error" : "success"}`}>{message}</p>}
    </div>
  );
};

export default GenerateKeys;