import { useState, useEffect,useCallback} from "react";
import axios from "axios";

const DownloadResults = () => {
  const [results, setResults] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [filterType, setFilterType] = useState("all");

  const fetchResults = useCallback(async () => {
    setIsLoading(true);
    setError("");
    try {

      // const response = await axios.get(`http://localhost:5000/download-results?filter=${filterType}`);
      
      const apiUrl = process.env.REACT_APP_API_URL; // for docker deploy with env
      const response = await axios.get(`${apiUrl}/download-results?filter=${filterType}`);
      setResults(response.data.results);
    } catch (error) {
      setError("Error fetching results. Please make sure all previous steps are completed.");
      console.error("Error fetching results:", error);
    } finally {
      setIsLoading(false);
    }
  }, [filterType]);

  useEffect(() => {
    fetchResults();
  }, [fetchResults]);

  const handleFilterChange = (e) => {
    setFilterType(e.target.value);
  };

  const handleDownloadCSV = () => {
    if (results.length === 0) return;

    // Create filename based on filter type
    const filename =
      filterType === "selected"
        ? "selected_parameter_analysis.csv"
        : "all_parameters_analysis.csv";

    // Create CSV header
    const header = [
      "Poly Mod Degree",
      "Coeff Mod Bit Sizes",
      "Key Gen Time",
      "Encrypt Time",
      "Plain Compute Time",
      "Encrypted Compute Time",
      "Plain Accuracy",
      "Plain Precision",
      "Plain Recall",
      "Plain F1",
      "Encrypted Accuracy",
      "Encrypted Precision",
      "Encrypted Recall",
      "Encrypted F1"
    ].join(",");

    // Create CSV content
    const csvContent =
      header +
      "\n" +
      results
        .map((result) =>
          [
            result.poly_mod_degree,
            JSON.stringify(result.coeff_mod_bit_sizes),
            result.key_gen_time,
            result.encrypt_time,
            result.plain_compute_time,
            result.encrypted_compute_time,
            result.plain_accuracy,
            result.plain_precision,
            result.plain_recall,
            result.plain_f1,
            result.encrypted_accuracy,
            result.encrypted_precision,
            result.encrypted_recall,
            result.encrypted_f1
          ].join(",")
        )
        .join("\n");

    // Create and download CSV
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", filename);

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="container">
      <h2>Analysis Results</h2>
      <p>View and download parameter analysis results.</p>

      <div className="parameter-section">
        <h3>Filter Options</h3>
        <div className="form-group">
          <label>
            Filter Results:
            <select value={filterType} onChange={handleFilterChange}>
              <option value="all">All Results</option>
              <option value="selected">My Selected Parameters</option>
            </select>
          </label>
        </div>
      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          gap: "10px",
          marginBottom: "20px"
        }}
      >
        <button onClick={fetchResults} disabled={isLoading}>
          {isLoading ? "Loading..." : "Refresh Results"}
        </button>
        {results.length > 0 && (
          <button onClick={handleDownloadCSV}>Download CSV</button>
        )}
      </div>

      {isLoading && (
        <div className="progress-container">
          <div className="progress-bar active"></div>
        </div>
      )}

      {error && <p className="message error">{error}</p>}

      {results.length > 0 ? (
        <div className="result">
          <h3>
            Parameter Analysis{" "}
            {filterType === "selected"
              ? "(Your Selected Parameters)"
              : "(All Parameters)"}
          </h3>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th>Poly Mod Degree</th>
                <th>Coeff Mod Bit Sizes</th>
                <th>Key Gen Time (s)</th>
                <th>Encrypt Time (s)</th>
                <th>Plain Compute (s)</th>
                <th>Encrypted Compute (s)</th>
                <th>Plain Accuracy</th>
                <th>Plain Precision</th>
                <th>Plain Recall</th>
                <th>Plain F1</th>
                <th>Encrypted Accuracy</th>
                <th>Encrypted Precision</th>
                <th>Encrypted Recall</th>
                <th>Encrypted F1</th>
              </tr>
            </thead>
            <tbody>
              {results.map((result, index) => (
                <tr key={index}>
                  <td>{result.poly_mod_degree}</td>
                  <td>{JSON.stringify(result.coeff_mod_bit_sizes)}</td>
                  <td>{result.key_gen_time.toFixed(4)}</td>
                  <td>{result.encrypt_time.toFixed(4)}</td>
                  <td>{result.plain_compute_time.toFixed(4)}</td>
                  <td>{result.encrypted_compute_time.toFixed(4)}</td>
                  <td>{(result.plain_accuracy * 100).toFixed(2)}%</td>
                  <td>{(result.plain_precision * 100).toFixed(2)}%</td>
                  <td>{(result.plain_recall * 100).toFixed(2)}%</td>
                  <td>{(result.plain_f1 * 100).toFixed(2)}%</td>
                  <td>{(result.encrypted_accuracy * 100).toFixed(2)}%</td>
                  <td>{(result.encrypted_precision * 100).toFixed(2)}%</td>
                  <td>{(result.encrypted_recall * 100).toFixed(2)}%</td>
                  <td>{(result.encrypted_f1 * 100).toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : !isLoading && !error ? (
        <p className="message">
          {filterType === "selected"
            ? "No results available for your selected parameters. Make sure you've completed all the previous steps with your parameters."
            : "No results available. Make sure you've completed the previous steps."}
        </p>
      ) : null}
    </div>
  );
};

export default DownloadResults;
