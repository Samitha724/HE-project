//NavBar.jsx
import { Link } from "react-router-dom";

const NavBar = () => {
  return (
    <nav style={{ padding: "10px", background: "#333", color: "white" }}>
      <Link to="/" style={{ marginRight: "10px", color: "white" }}>Home</Link>
      <Link to="/upload-csv" style={{ marginRight: "10px", color: "white" }}>Upload</Link> {/*NEW LINK # (02-02-25) UPDATE fe 1*/}
      <Link to="/generate-keys" style={{ marginRight: "10px", color: "white" }}>Generate Keys</Link>
      <Link to="/encrypt" style={{ marginRight: "10px", color: "white" }}>Encrypt</Link>
      <Link to="/compute" style={{ color: "white" }}>Compute</Link>
       
    </nav>
  );
};

export default NavBar;
