document.getElementById("analyzeBtn").addEventListener("click", analyze);

async function analyze() {
  console.log("=== ANALYZE STARTED ===");

  const fileInput = document.getElementById("resumeInput");
  const jobText = document.getElementById("jobDescription").value;
  const resultBox = document.getElementById("resultBox");

  console.log("Selected File:", fileInput.files[0]);
  console.log("Job Description:", jobText);

  if (!fileInput.files[0] || !jobText) {
    alert("Please upload resume and enter job description.");
    return;
  }

  const formData = new FormData();
  formData.append("resume", fileInput.files[0]);
  formData.append("job_description", jobText);

  console.log("FormData prepared.");

  resultBox.innerHTML = "Analyzing...";

  try {
    console.log("Sending request to backend...");

    const response = await fetch("http://127.0.0.1:5000/process", {
      method: "POST",
      body: formData,
    });

    console.log("Response status:", response.status);

    const data = await response.json();

    console.log("=== BACKEND RESPONSE ===");
    console.log(data);

    if (!data) {
      resultBox.innerHTML = "No data returned from backend.";
      return;
    }

    resultBox.innerHTML = `
      <h3>Candidate: ${data.candidate_name}</h3>
      <h4>Company: ${data.company_name}</h4>
      <h3>Match Score: ${data.match_score}%</h3>
      <p><strong>Matched Skills:</strong> ${data.matched_skills.join(", ") || "None"}</p>
      <p><strong>Missing Skills:</strong> ${data.missing_skills.join(", ") || "None"}</p>
    `;
  } catch (error) {
    console.error("=== FETCH ERROR ===");
    console.error(error);
    resultBox.innerHTML = "Error connecting to backend.";
  }

  console.log("=== ANALYZE FINISHED ===");
}
