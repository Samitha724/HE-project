// import React from "react";
// import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import LandingPage from "./components/LandingPage";
// import DataUpload from "./components/DataUpload";
// import KeyGeneration from "./components/KeyGeneration";
// import DataEncryption from "./components/DataEncryption";
// import DataSubmission from "./components/DataSubmission";
// import Navigation from "./components/Navigation";
// import "./App.css";

// function App() {
//   return (
//     <Router>
//       <div className="App">
//       <Navigation /> 
//         <Routes>
//           <Route path="/" element={<LandingPage />} />
//           <Route path="/upload" element={<DataUpload />} />
//           <Route path="/generate-keys" element={<KeyGeneration />} />
//           <Route path="/encrypt" element={<DataEncryption />} />
//           <Route path="/submit" element={<DataSubmission />} />
//         </Routes>
//       </div>
//     </Router>
//   );
// }

// export default App
import './App.css';//for css 13
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import Home from "./components/Home";
import GenerateKeys from "./components/GenerateKeys";
import Encrypt from "./components/Encrypt";
import Compute from "./components/Compute";
import UploadCSV from "./components/UploadCSV"; // Import the new page # (02-02-25) UPDATE fe 1

function App() {
  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/generate-keys" element={<GenerateKeys />} />
        <Route path="/encrypt" element={<Encrypt />} />
        <Route path="/compute" element={<Compute />} />
        <Route path="/upload-csv" element={<UploadCSV />} /> {/* New Route # (02-02-25) UPDATE fe 1 */}
      </Routes>
    </Router>
  );
}

export default App;



