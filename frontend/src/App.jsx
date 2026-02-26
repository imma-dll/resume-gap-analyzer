import { useState } from "react";
import "./App.css";

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState("");

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
  };

  const handleAnalyze = () => {
    if (!resumeFile || !jobDescription) {
      alert("Please upload resume and paste job description.");
      return;
    }

    console.log("Resume File:", resumeFile);
    console.log("Job Description:", jobDescription);

    setResult("Analysis will appear here after backend integration.");
  };

  return (
    <div className="container">
      <h1>AI Resume Skill Gap Analyzer</h1>

      <div className="section">
        <label>Upload Resume (PDF)</label>
        <input type="file" accept=".pdf" onChange={handleFileChange} />
      </div>

      <div className="section">
        <label>Paste Job Description</label>
        <textarea
          rows="8"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste job description here..."
        />
      </div>

      <button className="analyze-btn" onClick={handleAnalyze}>
        Analyze
      </button>

      {result && (
        <div className="result-box">
          <h3>Result</h3>
          <p>{result}</p>
        </div>
      )}
    </div>
  );
}

export default App;
