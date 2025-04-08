import { useState } from "react";
import axios from "axios";

const Encrypt = () => {
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleEncrypt = async () => {
    setIsLoading(true);
    try {
      // const response = await axios.post("http://localhost:5000/encrypt",{
      //   headers: {
      //     "Content-Type": "application/json",
      //   },
      // });

      const apiUrl = process.env.REACT_APP_API_URL;//for docker deploy with env
      const response = await axios.post(`${apiUrl}/encrypt`,      
        {
          headers: {
            "Content-Type": "application/json",
          },
        });
        
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data.error || "Error encrypting dataset");
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <div className="container">
      <h2>Encrypt Dataset</h2>
      <p>Encrypt your uploaded dataset using the generated keys.</p>
      
      <button onClick={handleEncrypt} disabled={isLoading}>
        {isLoading ? "Encrypting..." : "Encrypt Dataset"}
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

export default Encrypt;



