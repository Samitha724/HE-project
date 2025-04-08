import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import Home from "./components/Home";
import GenerateKeys from "./components/GenerateKeys";
import Encrypt from "./components/Encrypt";
import Compute from "./components/Compute";
import UploadCSV from "./components/UploadCSV";
import Parameters from "./components/Parameters";
import DownloadResults from "./components/DownloadResults";

function App() {
  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload-csv" element={<UploadCSV />} />
        <Route path="/generate-keys" element={<GenerateKeys />} />
        <Route path="/parameters" element={<Parameters />} />
        <Route path="/encrypt" element={<Encrypt />} />
        <Route path="/compute" element={<Compute />} />
        <Route path="/download-results" element={<DownloadResults />} />
      </Routes>
    </Router>
  );
}

export default App;