from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pdfplumber
import sqlite3
import json
import re
import pandas as pd
from datetime import datetime
from text_processing import process_text

app = Flask(__name__)
CORS(app)


# --------------------------
# DATABASE SETUP
# --------------------------
def init_db():
    conn = sqlite3.connect("resume_scores.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            company_name TEXT,
            match_score REAL,
            matched_skills TEXT,
            missing_skills TEXT,
            total_resume_skills INTEGER,
            total_job_skills INTEGER,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# --------------------------
# TEXT EXTRACTION
# --------------------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


# --------------------------
# NAME EXTRACTION (Simple Heuristic)
# --------------------------
def extract_candidate_name(raw_text):
    lines = raw_text.split("\n")
    for line in lines:
        line = line.strip()
        if len(line) > 2 and len(line.split()) <= 4:
            return line
    return "N/A"


# --------------------------
# COMPANY EXTRACTION
# --------------------------
def extract_company_name(job_text):

    # Look for pattern like "Company: XYZ"
    match = re.search(r'company\s*:\s*(.+)', job_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Look for "Join XYZ"
    match = re.search(r'join\s+([A-Z][a-zA-Z0-9& ]+)', job_text)
    if match:
        return match.group(1).strip()

    return "N/A"


# --------------------------
# MAIN ROUTE
# --------------------------
@app.route("/process", methods=["POST"])
def process():

    print("\n=== NEW REQUEST RECEIVED ===")

    if "resume" not in request.files:
        print("ERROR: Resume file missing")
        return jsonify({"error": "Resume file missing"}), 400

    if "job_description" not in request.form:
        print("ERROR: Job description missing")
        return jsonify({"error": "Job description missing"}), 400

    resume_file = request.files["resume"]
    job_description = request.form["job_description"]

    print("Resume filename:", resume_file.filename)
    print("Job description length:", len(job_description))

    resume_raw = extract_text_from_pdf(resume_file)
    print("Extracted resume text length:", len(resume_raw))

    candidate_name = extract_candidate_name(resume_raw)
    company_name = extract_company_name(job_description)

    print("Detected candidate name:", candidate_name)
    print("Detected company name:", company_name)

    resume_processed = process_text(resume_raw)
    job_processed = process_text(job_description)

    print("Resume skills detected:", resume_processed["skills_detected"])
    print("Job skills detected:", job_processed["skills_detected"])

    resume_skills = {skill["skill"] for skill in resume_processed["skills_detected"]}
    job_skills = {skill["skill"] for skill in job_processed["skills_detected"]}

    matched_skills = list(resume_skills.intersection(job_skills))
    missing_skills = list(job_skills.difference(resume_skills))

    print("Matched skills:", matched_skills)
    print("Missing skills:", missing_skills)

    if len(job_skills) > 0:
        match_score = round((len(matched_skills) / len(job_skills)) * 100, 2)
    else:
        match_score = 0

    print("Match score:", match_score)

    conn = sqlite3.connect("resume_scores.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO scores (
            candidate_name,
            company_name,
            match_score,
            matched_skills,
            missing_skills,
            total_resume_skills,
            total_job_skills,
            timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_name,
        company_name,
        match_score,
        ", ".join(matched_skills),
        ", ".join(missing_skills),
        len(resume_skills),
        len(job_skills),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    print("Data saved to database.")

    response = {
        "candidate_name": candidate_name,
        "company_name": company_name,
        "match_score": match_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }

    print("Sending response:", response)
    print("=== REQUEST COMPLETED ===\n")

    return jsonify(response)
# --------------------------
# EXPORT TO EXCEL
# --------------------------
@app.route("/export", methods=["GET"])
def export_to_excel():

    conn = sqlite3.connect("resume_scores.db")
    df = pd.read_sql_query("SELECT * FROM scores", conn)
    conn.close()

    file_path = "resume_scores_export.xlsx"
    df.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)