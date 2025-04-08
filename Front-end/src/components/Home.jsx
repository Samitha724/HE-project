const Home = () => {
    return (
      <div className="container">
        <h1>Welcome to the Homomorphic Encryption Demo</h1>
        <p>Select an option from the navigation bar.</p>
        
        <div className="workflow-guide">
          <h3>Recommended Workflow:</h3>
          <ol>
            <li>Upload your CSV dataset</li>
            <li>Set encryption parameters</li>
            <li>Generate encryption keys</li>
            <li>Encrypt your dataset</li>
            <li>Run computations</li>
            <li>View or download results</li>
          </ol>
        </div>
      </div>
    );
  };
  
  export default Home;