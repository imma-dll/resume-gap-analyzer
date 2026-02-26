document.getElementById("analyzeBtn").addEventListener("click", analyze);

async function analyze() {
  const fileInput = document.getElementById("resumeInput");
  const jobText = document.getElementById("jobDescription").value;
  const resultBox = document.getElementById("resultBox");

  if (!fileInput.files[0] || !jobText) {
    alert("Upload resume and paste job description.");
    return;
  }

  const formData = new FormData();
  formData.append("resume", fileInput.files[0]);
  formData.append("job_description", jobText);

  resultBox.innerHTML = "Analyzing...";

  try {
    const response = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    resultBox.innerHTML = `
            <h3>Match Score: ${data.match_score}%</h3>
            <p><strong>Matched Skills:</strong> ${data.matched_skills.join(", ")}</p>
            <p><strong>Missing Skills:</strong> ${data.missing_skills.join(", ")}</p>
        `;
  } catch (error) {
    resultBox.innerHTML = "Error connecting to backend.";
    console.error(error);
    resultBox.innerHTML = "Analyzing...";
  }
}
