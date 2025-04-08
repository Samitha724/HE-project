import React, { useState, useEffect } from "react";
import axios from "axios";

const Parameters = () => {
  const [parameters, setParameters] = useState([]);
  const [selectedParamIndex, setSelectedParamIndex] = useState("");
  const [customPolyModDegree, setCustomPolyModDegree] = useState(8192);
  const [customCoeffModBitSizes, setCustomCoeffModBitSizes] = useState("60, 40, 60");
  const [usePredefined, setUsePredefined] = useState(true); // Track which parameter input to use
  const [message, setMessage] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchParameters();
  }, []);

  const fetchParameters = async () => {
    setIsLoading(true);
    try {
      // const response = await axios.get("http://localhost:5000/parameters");

      const apiUrl = process.env.REACT_APP_API_URL;//for docker deploy with env
      const response = await axios.get(`${apiUrl}/parameters`);

      setParameters(response.data.parameters);
      if (response.data.parameters.length > 0) {
        setSelectedParamIndex(0); // Select the first parameter set by default
      }
    } catch (error) {
      setMessage("Error fetching parameters.");
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSetParameters = async () => {
    setIsLoading(true);
    try {
      let paramToSend;

      if (usePredefined) {
        paramToSend = parameters[selectedParamIndex];
      } else {
        paramToSend = {
          poly_mod_degree: parseInt(customPolyModDegree),
          coeff_mod_bit_sizes: customCoeffModBitSizes
            .split(",")
            .map((x) => parseInt(x.trim())),
        };
      }
      console.log("Sending parameters to backend:", paramToSend); // cheking request
      // const response = await axios.post("http://localhost:5000/set-parameters", paramToSend);

      const apiUrl = process.env.REACT_APP_API_URL;//for docker deploy with env
      const response = await axios.post(`${apiUrl}/set-parameters`, paramToSend);

      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data.error || "Error setting parameters.");
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Encryption Parameters</h2>
      <p>Select parameters to use for encryption.</p>

      <div>
        <label>
          <input
            type="radio"
            value="predefined"
            checked={usePredefined}
            onChange={() => setUsePredefined(true)}
          />
          Use Predefined Parameters
        </label>
        <label>
          <input
            type="radio"
            value="custom"
            checked={!usePredefined}
            onChange={() => setUsePredefined(false)}
          />
          Use Custom Parameters
        </label>
      </div>

      {usePredefined ? (
        <div>
          <select
            value={selectedParamIndex}
            onChange={(e) => setSelectedParamIndex(parseInt(e.target.value))}
          >
            {parameters.map((param, index) => (
              <option key={index} value={index}>
                Poly Mod: {param.poly_mod_degree}, Coeff Mod:{" "}
                {JSON.stringify(param.coeff_mod_bit_sizes)}
              </option>
            ))}
          </select>
        </div>
      ) : (
        <div>
          <label>
            Polynomial Modulus Degree:
            <input
              type="number"
              value={customPolyModDegree}
              onChange={(e) => setCustomPolyModDegree(e.target.value)}
            />
          </label>
          <label>
            Coefficient Modulus Bit Sizes (comma separated):
            <input
              type="text"
              value={customCoeffModBitSizes}
              onChange={(e) => setCustomCoeffModBitSizes(e.target.value)}
              placeholder="e.g., 60, 40, 60"
            />
          </label>
        </div>
      )}

      <button onClick={handleSetParameters} disabled={isLoading}>
        Set Parameters
      </button>

      {isLoading && (
        <div className="progress-container">
          <div className="progress-bar active"></div>
        </div>
      )}

      {message && (
        <p className={`message ${message.includes("Error") ? "error" : "success"}`}>
          {message}
        </p>
      )}
    </div>
  );
};

export default Parameters;
