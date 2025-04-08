import { useState } from "react";
import axios from "axios";

const Compute = () => {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleCompute = async () => {
    setIsLoading(true);
    setError("");
    try {

      // const response = await axios.get("http://localhost:5000/compute");
      const apiUrl = process.env.REACT_APP_API_URL;//for docker deploy with env
      const response = await axios.get(`${apiUrl}/compute`);
      
      setResults(response.data);
    } catch (error) {
      setError(error.response?.data.error || "Error running computation");
      console.error("Computation error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Run Encrypted Computation</h2>
      <p>
        Run computations on both encrypted and plain data to compare metrics.
      </p>

      <button onClick={handleCompute} disabled={isLoading}>
        {isLoading ? "Computing..." : "Run Computation"}
      </button>

      {isLoading && (
        <div className="progress-container">
          <div className="progress-bar active"></div>
        </div>
      )}

      {error && <p className="message error">{error}</p>}

      {results && (
        <div className="result">
          <h3>Computation Results</h3>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th>Metric</th>
                <th>Plain</th>
                <th>Encrypted</th>
                <th>Difference</th>
              </tr>
            </thead>
            <tbody>
              {["accuracy", "precision", "recall", "f1"].map((metric) => (
                <tr key={metric}>
                  <td>{metric.charAt(0).toUpperCase() + metric.slice(1)}</td>
                  <td>{(results.plain_metrics[metric] * 100).toFixed(2)}%</td>
                  <td>{(results.encrypted_metrics[metric] * 100).toFixed(2)}%</td>
                  <td>{(results.difference_metrics[metric] * 100).toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className="message success">{results.message}</p>
        </div>
      )}
    </div>
  );
};

export default Compute;
