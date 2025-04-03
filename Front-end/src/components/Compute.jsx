// import axios from "axios";
// import { useState } from "react";

// const Compute = () => {

//   const [computationResult, setComputationResult] = useState("");

//   const [isLoading, setIsLoading] = useState(false);

//   const handleCompute = async () => {
//     setIsLoading(true);
//     try {
//       const response = await axios.get("http://127.0.0.1:5000/compute");
//       setComputationResult(
//         `Encrypted Accuracy: ${response.data.encrypted_accuracy}, Difference: ${response.data.diff_accuracy}`
//       );
//     } catch (error) {
//       setComputationResult(error.response?.data.error || "Error performing computation");
//     }
//     setIsLoading(false);
//   };
  
//   return (
//     <div className="container">
//       <h2>Compute on Encrypted Data</h2>
//       <button onClick={handleCompute} disabled={isLoading}>
//         Compute
//       </button>
//       {isLoading && (
//         <div className="progress-container">
//           <div className="progress-bar active"></div>
//         </div>
//       )}
//       {computationResult && <div className="result">{computationResult}</div>}
//     </div>
//   );};



// export default Compute;

// this 3-6 from upabove upto this 


// import axios from "axios";
// import { useState } from "react";

// const Compute = () => {
//   const [computationResult, setComputationResult] = useState("");

//   const handleCompute = async () => {
//     try {
//       // Call the /compute endpoint
//       const response = await axios.post("http://127.0.0.1:5000/compute");

//       // Set the result from the response
//       if (response.data.diff_accuracy !== undefined) {
//         setComputationResult(`Difference in accuracy: ${response.data.diff_accuracy}`);
//       } else {
//         setComputationResult("No result returned");
//       }
//     } catch (error) {
//       console.error("Error:", error.response?.data || error.message);
//       setComputationResult("Error during computation");
//     }
//   };

//   return (
//     <div style={{ textAlign: "center", marginTop: "20px" }}>
//       <h2>Compute Accuracy Difference</h2>
//       <button onClick={handleCompute} style={{ padding: "10px", cursor: "pointer" }}>
//         Compute Difference
//       </button>
//       <p>{computationResult}</p>
//     </div>
//   );
// };

// export default Compute;
//3-26 dateupdate
// import axios from "axios";
// import { useState } from "react";

// const Compute = () => {
//   const [computationResult, setComputationResult] = useState("");
//   const [resultData, setResultData] = useState(null);

//   const handleCompute = async () => {
//     try {
//       const response = await axios.get("http://127.0.0.1:5000/compute");
      
//       // Store the full result data for download
//       setResultData({
//         encrypted_accuracy: response.data.encrypted_accuracy,
//         diff_accuracy: response.data.diff_accuracy
//       });
      
//       // Display the result
//       setComputationResult(
//         `Encrypted Accuracy: ${response.data.encrypted_accuracy}, Difference: ${response.data.diff_accuracy}`
//       ); 
      
//     } catch (error) {
//       setComputationResult(error.response?.data.error || "Error performing computation");
//       setResultData(null);
//     }
//   };

//   const handleDownload = () => {
//     if (!resultData) return;
    
//     // Create a CSV string with the result data
//     const csvContent = 
//       "Metric,Value\n" +
//       `Encrypted Accuracy,${resultData.encrypted_accuracy}\n` +
//       `Accuracy Difference,${resultData.diff_accuracy}`;
    
//     // Create a Blob with the CSV content
//     const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8" });
    
//     // Create a download link
//     const url = URL.createObjectURL(blob);
//     const link = document.createElement("a");
//     link.href = url;
//     link.setAttribute("download", "accuracy_results.csv");
    
//     // Append the link to the body, click it, and remove it
//     document.body.appendChild(link);
//     link.click();
//     document.body.removeChild(link);
//   };

//   return (
//     <div style={{ textAlign: "center", marginTop: "20px" }}>
//       <h2>Compute on Encrypted Data</h2>
//       <button 
//         onClick={handleCompute} 
//         style={{ padding: "10px", cursor: "pointer", marginRight: "10px" }}
//       >
//         Compute
//       </button>
      
//       {resultData && (
//         <button 
//           onClick={handleDownload} 
//           style={{ 
//             padding: "10px", 
//             cursor: "pointer", 
//             backgroundColor: "#4CAF50", 
//             color: "white", 
//             border: "none", 
//             borderRadius: "4px" 
//           }}
//         >
//           Download Results
//         </button>
//       )}
      
//       <p>Result: {computationResult}</p>
//     </div>
//   );
// };

// export default Compute;

// //3-26 new 1 ()
// import axios from "axios";
// import { useState } from "react";

// const Compute = () => {
//   const [computationResults, setComputationResults] = useState([]);
//   const [isLoading, setIsLoading] = useState(false);

//   const handleCompute = async () => {
//     setIsLoading(true);
//     try {
//       const response = await axios.get("http://127.0.0.1:5000/generate-keys");
//       setComputationResults(response.data.results);
//     } catch (error) {
//       console.error("Computation error:", error);
//       setComputationResults([]);
//     }
//     setIsLoading(false);
//   };

//   const handleDownload = () => {
//     if (computationResults.length === 0) return;
    
//     // Create CSV content
//     const csvContent = 
//       "Poly Mod Degree,Coeff Mod Bit Sizes,Train Time,Key Gen Time,Encrypt Time,Compute Time,Plain Accuracy,Encrypted Accuracy\n" +
//       computationResults.map(result => 
//         `${result.poly_mod_degree},"${result.coeff_mod_bit_sizes}",${result.train_time},${result.key_gen_time},${result.encrypt_time},${result.compute_time},${result.plain_accuracy},${result.encrypted_accuracy}`
//       ).join("\n");
    
//     // Create and download CSV
//     const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8" });
//     const url = URL.createObjectURL(blob);
//     const link = document.createElement("a");
//     link.href = url;
//     link.setAttribute("download", "encryption_parameter_analysis.csv");
    
//     document.body.appendChild(link);
//     link.click();
//     document.body.removeChild(link);
//   };

//   return (
//     <div className="container">
//       <h2>Encryption Parameter Analysis</h2>
//       <div style={{ display: 'flex', justifyContent: 'center', gap: '10px' }}>
//         <button onClick={handleCompute} disabled={isLoading}>
//           {isLoading ? 'Analyzing...' : 'Analyze Parameters'}
//         </button>
//         {computationResults.length > 0 && (
//           <button onClick={handleDownload}>
//             Download Results
//           </button>
//         )}
//       </div>

//       {isLoading && (
//         <div className="progress-container">
//           <div className="progress-bar active"></div>
//         </div>
//       )}

//       {computationResults.length > 0 && (
//         <div className="result">
//           <h3>Analysis Results</h3>
//           <table style={{ width: '100%', borderCollapse: 'collapse' }}>
//             <thead>
//               <tr>
//                 <th>Poly Mod Degree</th>
//                 <th>Coeff Mod Bit Sizes</th>
//                 <th>Plain Accuracy</th>
//                 <th>Encrypted Accuracy</th>
//               </tr>
//             </thead>
//             <tbody>
//               {computationResults.map((result, index) => (
//                 <tr key={index}>
//                   <td>{result.poly_mod_degree}</td>
//                   <td>{JSON.stringify(result.coeff_mod_bit_sizes)}</td>
//                   <td>{result.plain_accuracy.toFixed(4)}</td>
//                   <td>{result.encrypted_accuracy.toFixed(4)}</td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>
//       )}
//     </div>
//   );
// };

// export default Compute;

//3-26-25 new 2
// import axios from "axios";
// import { useState } from "react";

// const Compute = () => {
//   const [computationResults, setComputationResults] = useState([]);
//   const [isLoading, setIsLoading] = useState(false);

//   const handleCompute = async () => {
//     setIsLoading(true);
//     try {
//       const response = await axios.get("http://127.0.0.1:5000/generate-keys");
//       setComputationResults(response.data.results);
//     } catch (error) {
//       console.error("Computation error:", error);
//       setComputationResults([]);
//     }
//     setIsLoading(false);
//   };

//   const handleDownload = () => {
//     if (computationResults.length === 0) return;
    
//     // Create CSV content
//     const csvContent = 
//       "Poly Mod Degree,Coeff Mod Bit Sizes,Train Time,Key Gen Time,Encrypt Time,Compute Time,Plain Accuracy,Encrypted Accuracy\n" +
//       computationResults.map(result => 
//         `${result.poly_mod_degree},"${result.coeff_mod_bit_sizes}",${result.train_time},${result.key_gen_time},${result.encrypt_time},${result.compute_time},${result.plain_accuracy},${result.encrypted_accuracy}`
//       ).join("\n");
    
//     // Create and download CSV
//     const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8" });
//     const url = URL.createObjectURL(blob);
//     const link = document.createElement("a");
//     link.href = url;
//     link.setAttribute("download", "encryption_parameter_analysis.csv");
    
//     document.body.appendChild(link);
//     link.click();
//     document.body.removeChild(link);
//   };

//   return (
//     <div className="container">
//       <h2>Encryption Parameter Analysis</h2>
//       <div style={{ display: 'flex', justifyContent: 'center', gap: '10px' }}>
//         <button onClick={handleCompute} disabled={isLoading}>
//           {isLoading ? 'Analyzing...' : 'Analyze Parameters'}
//         </button>
//         {computationResults.length > 0 && (
//           <button onClick={handleDownload}>
//             Download Results
//           </button>
//         )}
//       </div>

//       {isLoading && (
//         <div className="progress-container">
//           <div className="progress-bar active"></div>
//         </div>
//       )}

//       {computationResults.length > 0 && (
//         <div className="result">
//           <h3>Analysis Results</h3>
//           <table style={{ width: '100%', borderCollapse: 'collapse' }}>
//             <thead>
//               <tr>
//                 <th>Poly Mod Degree</th>
//                 <th>Coeff Mod Bit Sizes</th>
//                 <th>Plain Accuracy</th>
//                 <th>Encrypted Accuracy</th>
//               </tr>
//             </thead>
//             <tbody>
//               {computationResults.map((result, index) => (
//                 <tr key={index}>
//                   <td>{result.poly_mod_degree}</td>
//                   <td>{JSON.stringify(result.coeff_mod_bit_sizes)}</td>
//                   <td>{result.plain_accuracy.toFixed(4)}</td>
//                   <td>{result.encrypted_accuracy.toFixed(4)}</td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>
//       )}
//     </div>
//   );
// };

// export default Compute;

//Compute.jsx

import { useState } from "react";

const Compute = () => {
  const [computationResults, setComputationResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleCompute = async () => {
    setIsLoading(true);
    try {
      // const response = await fetch("http://127.0.0.1:5000/generate-keys");//for local host
      // const response = await fetch("https://heproject-backend-575598110807.asia-south1.run.app/generate-keys");//for docker deploy  
      const apiUrl = process.env.REACT_APP_API_URL;//for docker deploy with env
      const response = await fetch(`${apiUrl}/generate-keys`);//for docker deploy with env


      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || "Error generating keys");
      }
      
      setComputationResults(data.results);
    } catch (error) {
      console.error("Computation error:", error);
      setComputationResults([]);
    }
    setIsLoading(false);
  };

  const handleDownload = () => {
    if (computationResults.length === 0) return;
    
    // Create CSV content
    const csvContent = 
      "Poly Mod Degree,Coeff Mod Bit Sizes,Train Time,Key Gen Time,Encrypt Time,Plain Compute Time,Encrypted Compute Time,Plain Accuracy,Encrypted Accuracy\n" +
      computationResults.map(result => 
        `${result.poly_mod_degree},"${result.coeff_mod_bit_sizes}",${result.train_time},${result.key_gen_time},${result.encrypt_time},${result.plain_compute_time},${result.encrypted_compute_time},${result.plain_accuracy},${result.encrypted_accuracy}`
      ).join("\n");
    
    // Create and download CSV
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "encryption_parameter_analysis.csv");
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="container">
      <h2>Encryption Parameter Analysis</h2>
      <div style={{ display: 'flex', justifyContent: 'center', gap: '10px' }}>
        <button onClick={handleCompute} disabled={isLoading}>
          {isLoading ? 'Analyzing...' : 'Analyze Parameters'}
        </button>
        {computationResults.length > 0 && (
          <button onClick={handleDownload}>
            Download Results
          </button>
        )}
      </div>

      {isLoading && (
        <div className="progress-container">
          <div className="progress-bar active"></div>
        </div>
      )}

      {computationResults.length > 0 && (
        <div className="result">
          <h3>Analysis Results</h3>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th>Poly Mod Degree</th>
                <th>Coeff Mod Bit Sizes</th>
                <th>Train Time (s)</th>
                <th>Key Gen Time (s)</th>
                <th>Encrypt Time (s)</th>
                <th>Plain Compute Time (s)</th>
                <th>Encrypted Compute Time (s)</th>
                <th>Plain Accuracy</th>
                <th>Encrypted Accuracy</th>
              </tr>
            </thead>
            <tbody>
              {computationResults.map((result, index) => (
                <tr key={index}>
                  <td>{result.poly_mod_degree}</td>
                  <td>{JSON.stringify(result.coeff_mod_bit_sizes)}</td>
                  <td>{result.train_time.toFixed(4)}</td>
                  <td>{result.key_gen_time.toFixed(4)}</td>
                  <td>{result.encrypt_time.toFixed(4)}</td>
                  <td>{result.plain_compute_time.toFixed(4)}</td>
                  <td>{result.encrypted_compute_time.toFixed(4)}</td>
                  <td>{result.plain_accuracy.toFixed(4)}</td>
                  <td>{result.encrypted_accuracy.toFixed(4)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Compute;

// //Compute.jsx 4and for 2nd

// import { useState } from "react";

// const Compute = () => {
//   const [computationResults, setComputationResults] = useState([]);
//   const [isLoading, setIsLoading] = useState(false);

//   const handleCompute = async () => {
//     setIsLoading(true);
//     try {
//       const response = await fetch("http://127.0.0.1:5000/compute");
//       const data = await response.json();
      
//       if (!response.ok) {
//         throw new Error(data.error || "Error computing results");
//       }
      
//       setComputationResults([data]);
//     } catch (error) {
//       console.error("Computation error:", error);
//       setComputationResults([]);
//     }
//     setIsLoading(false);
//   };

//   const handleDownload = () => {
//     if (computationResults.length === 0) return;
    
//     // Create CSV content
//     const csvContent = 
//       "Plain Accuracy,Encrypted Accuracy,Accuracy Difference,Noise Variance,Noise Standard Deviation\n" +
//       computationResults.map(result => 
//         `${result.plain_accuracy},${result.encrypted_accuracy},${result.diff_accuracy},${result.noise_variance},${result.noise_std_dev}`
//       ).join("\n");
    
//     // Create and download CSV
//     const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8" });
//     const url = URL.createObjectURL(blob);
//     const link = document.createElement("a");
//     link.href = url;
//     link.setAttribute("download", "noise_analysis_results.csv");
    
//     document.body.appendChild(link);
//     link.click();
//     document.body.removeChild(link);
//   };

//   return (
//     <div className="container">
//       <h2>Homomorphic Encryption Noise Analysis</h2>
//       <div style={{ display: 'flex', justifyContent: 'center', gap: '10px' }}>
//         <button onClick={handleCompute} disabled={isLoading}>
//           {isLoading ? 'Analyzing...' : 'Analyze Noise'}
//         </button>
//         {computationResults.length > 0 && (
//           <button onClick={handleDownload}>
//             Download Results
//           </button>
//         )}
//       </div>

//       {isLoading && (
//         <div className="progress-container">
//           <div className="progress-bar active"></div>
//         </div>
//       )}

//       {computationResults.length > 0 && (
//         <div className="result">
//           <h3>Noise Analysis Results</h3>
//           <table style={{ width: '100%', borderCollapse: 'collapse' }}>
//             <thead>
//               <tr>
//                 <th>Plain Accuracy</th>
//                 <th>Encrypted Accuracy</th>
//                 <th>Accuracy Difference</th>
//                 <th>Noise Variance</th>
//                 <th>Noise Std Deviation</th>
//               </tr>
//             </thead>
//             <tbody>
//               {computationResults.map((result, index) => (
//                 <tr key={index}>
//                   <td>{result.plain_accuracy.toFixed(4)}</td>
//                   <td>{result.encrypted_accuracy.toFixed(4)}</td>
//                   <td>{result.diff_accuracy.toFixed(4)}</td>
//                   <td>{result.noise_variance.toFixed(6)}</td>
//                   <td>{result.noise_std_dev.toFixed(6)}</td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         </div>
//       )}
//     </div>
//   );
// };

// export default Compute;