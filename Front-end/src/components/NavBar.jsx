import { Link } from "react-router-dom";

const NavBar = () => {
  return (
    <nav>
      <Link to="/">Home</Link>
      <Link to="/upload-csv">Upload</Link>
      <Link to="/parameters">Parameters</Link>
      <Link to="/generate-keys">Generate Keys</Link>
      <Link to="/encrypt">Encrypt</Link>
      <Link to="/compute">Compute</Link>
      <Link to="/download-results">Results</Link>
    </nav>
  );
};

export default NavBar;