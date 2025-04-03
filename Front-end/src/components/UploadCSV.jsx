//UploadCSV.jsx
import { useState } from "react";
import axios from "axios";

function UploadCSV() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  // Handle file selection
  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a CSV file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      // const response = await axios.post("http://localhost:5000/upload", formData, { //for local host
      //   headers: { "Content-Type": "multipart/form-data" },  //for local host

      // const response = await axios.post("https://heproject-backend-575598110807.asia-south1.run.app/upload", formData, { //for docker deploy
      //   headers: { "Content-Type": "multipart/form-data" },     //for docker deploy
      const apiUrl = process.env.REACT_APP_API_URL;
      const response = await axios.post(`${apiUrl}/upload`, formData, { //for docker deploy with env
        headers: { "Content-Type": "multipart/form-data" },     //for docker deploy with env
      
      });

      setMessage(response.data.message);//massage from backend check1
      
    //   //# (02-02-25) UPDATE fe 4<
    //   // After successful file upload, call the encryption endpoint
    //   if (response.data.message === "File uploaded successfully") {
    //     // Now, send the filename to the /encrypt endpoint
    //     const encryptionResponse = await axios.post("http://localhost:5000/encrypt", {
    //       filename: file.name, // Send the uploaded filename
    //     });

    //     // Display the response from the encryption
    //     setMessage(encryptionResponse.data.message);
    //   }
    //   //# (02-02-25) UPDATE fe 4>

    } catch (error) {
    //   setMessage("Error uploading file.");# check 1 comented and below line to get backend error
      setMessage(error.response?.data.error || "Error uploading file.");
      console.error("Upload Error:", error);
    }
  };
//css 13<
  return (
    <div className="container">
      <h2>Upload CSV File</h2>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {message && <p className={`message ${message.includes("Error") ? "error" : "success"}`}>{message}</p>}
    </div>
  );//css 13
}

export default UploadCSV;


