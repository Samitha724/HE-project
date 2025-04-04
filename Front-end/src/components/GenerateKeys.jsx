//GenerateKeys.jsx
import axios from "axios";
import { useState } from "react";

const GenerateKeys = () => {
  const [message, setMessage] = useState("");

  const handleGenerateKeys = async () => {
    try {
      // const response = await axios.get("http://127.0.0.1:5000/generate-keys");//for local host
      // const response = await axios.get("https://heproject-backend-575598110807.asia-south1.run.app/generate-keys");//For docker deploy
      const apiUrl = process.env.REACT_APP_API_URL;//for docker deploy with env
      const response = await axios.get(`${apiUrl}/generate-keys`);//for docker deploy with env


      setMessage(response.data.message);//check1 display backend massage
    } catch (error) {
      setMessage(error.response?.data.error || "Error generating keys");//check1 updated this line to display backend massage
    }
  };
  //css13
  return (
    <div className="container">
      <h2>Generate HE Keys</h2>
      <button onClick={handleGenerateKeys}>
        Generate Keys
      </button>
      {message && <p className={`message ${message.includes("Error") ? "error" : "success"}`}>{message}</p>}
    </div>
  );//css13
};

export default GenerateKeys;
