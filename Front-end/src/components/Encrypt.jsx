// import axios from "axios";
// import { useState } from "react";

// const Encrypt = () => {
//   const [plaintext, setPlaintext] = useState("");
//   const [encryptedData, setEncryptedData] = useState("");

//   const handleEncrypt = async () => {
//     try {
//       const response = await axios.post("http://127.0.0.1:5000/encrypt", { data: plaintext });
//       setEncryptedData(response.data.encrypted);
//     } catch (error) {
//       setEncryptedData("Error encrypting data");
//     }
//   };

//   return (
//     <div style={{ textAlign: "center", marginTop: "20px" }}>
//       <h2>Encrypt Data</h2>
//       <input
//         type="text"
//         placeholder="Enter data to encrypt"
//         value={plaintext}
//         onChange={(e) => setPlaintext(e.target.value)}
//         style={{ padding: "5px" }}
//       />
//       <button onClick={handleEncrypt} style={{ padding: "10px", marginLeft: "10px", cursor: "pointer" }}>
//         Encrypt
//       </button>
//       <p>Encrypted: {encryptedData}</p>
//     </div>
//   );
// };

// export default Encrypt;


// import axios from "axios";
// import { useState } from "react";

// const Encrypt = () => {
//   const [message, setMessage] = useState("");

//   const handleEncrypt = async () => {
//     try {
//       const response = await axios.post("http://127.0.0.1:5000/encrypt");
//       setMessage(response.data.message || "Encryption successful");
//     } catch (error) {
//       console.error("Error:", error.response?.data || error.message);
//       setMessage("Error encrypting dataset");
//     }
//   };

//   return (
//     <div style={{ textAlign: "center", marginTop: "20px" }}>
//       <h2>Encrypt Dataset</h2>
//       <button onClick={handleEncrypt} style={{ padding: "10px", cursor: "pointer" }}>
//         Encrypt Dataset
//       </button>
//       <p>{message}</p>
//     </div>
//   );
// };

// export default Encrypt;


import axios from "axios";
import { useState } from "react";

const Encrypt = () => {

  const [message, setMessage] = useState("");
  
  const [isLoading, setIsLoading] = useState(false);

  const handleEncrypt = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post("http://127.0.0.1:5000/encrypt");
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data.error || "Error encrypting dataset");
    }
    setIsLoading(false);
  };
  
  return (
    <div className="container">
      <h2>Encrypt Dataset</h2>
      <button onClick={handleEncrypt} disabled={isLoading}>
        Encrypt Dataset
      </button>
      {isLoading && (
        <div className="progress-container">
          <div className="progress-bar active"></div>
        </div>
      )}
      {message && <p className={`message ${message.includes("Error") ? "error" : "success"}`}>{message}</p>}
    </div>
  );};



export default Encrypt;
