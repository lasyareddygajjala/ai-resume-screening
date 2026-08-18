from pdf_generator import generate_pdf
from PyPDF2 import PdfReader
from io import BytesIO
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import asyncio
import time

app = FastAPI()

# 🔥 VERY IMPORTANT (FIXES ERROR)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def generate_result(text, filename, job_description, category):

    resume_text = text.lower()
    # Resume Summary Detection
    candidate_name = filename.replace(".pdf", "")

    education = "Not Found"
    if "b.tech" in resume_text:
        education = "B.Tech"
    elif "m.tech" in resume_text:
        education = "M.Tech"
    elif "b.e" in resume_text:
        education = "B.E"

    experience = "Fresher"
    if "experience" in resume_text:
        experience = "Experienced"

    projects = 0
    if "projects" in resume_text:
        projects = resume_text.count("1.") + resume_text.count("2.") + resume_text.count("3.")

    certifications = 0
    if "certification" in resume_text or "certifications" in resume_text:
        certifications = 2
    jd_text = job_description.lower()

        # =====================================================
    # SMART SKILL MATCHING
    # =====================================================

    skill_aliases = {

        "python": ["python", "python3"],

        "java": ["java", "java programming"],

        "c++": ["c++", "cpp"],

        "sql": ["sql", "structured query language"],

        "mysql": ["mysql"],

        "mongodb": ["mongodb", "mongo db"],

        "fastapi": ["fastapi"],

        "flask": ["flask"],

        "django": ["django"],

        "html": ["html", "html5"],

        "css": ["css", "css3"],

        "javascript": [
            "javascript",
            "java script",
            "js",
            "ecmascript"
        ],

        "react": [
            "react",
            "reactjs",
            "react.js"
        ],

        "node.js": [
            "node.js",
            "nodejs",
            "node js"
        ],

        "git": ["git"],

        "github": [
            "github",
            "git hub"
        ],

        "docker": ["docker"],

        "aws": [
            "aws",
            "amazon web services"
        ],

        "linux": ["linux"],

        "tensorflow": ["tensorflow"],

        "pytorch": ["pytorch"],

        "machine learning": [
            "machine learning",
            "machine-learning",
            "ml"
        ],

        "deep learning": [
            "deep learning",
            "deep-learning",
            "dl"
        ],

        "pandas": ["pandas"],

        "numpy": ["numpy"],

        "opencv": [
            "opencv",
            "open cv"
        ],

        "rest api": [
            "rest api",
            "rest apis",
            "restful api",
            "restful apis",
            "rest-api"
        ],

        "data structures": [
            "data structures",
            "data structure",
            "dsa",
            "data structures and algorithms",
            "data structures & algorithms"
        ]
    }


    # Normalize text
    jd_text = jd_text.lower()
    resume_text = resume_text.lower()


    # Find required skills in Job Description
    jd_skills = []

    for skill, aliases in skill_aliases.items():

        for alias in aliases:

            if alias in jd_text:
                jd_skills.append(skill)
                break


    # Find matching skills in Resume
    matched_skills = []

    for skill in jd_skills:

        aliases = skill_aliases[skill]

        if any(alias in resume_text for alias in aliases):
            matched_skills.append(skill)


    # Find missing skills
    missing_skills = [
        skill
        for skill in jd_skills
        if skill not in matched_skills
    ]


    # Remove duplicates while preserving order
    jd_skills = list(dict.fromkeys(jd_skills))
    matched_skills = list(dict.fromkeys(matched_skills))
    missing_skills = list(dict.fromkeys(missing_skills))

    # ==============================
    # PROFESSIONAL ATS SCORE
    # ==============================

    # 1. Skills Score - 60%
    if len(jd_skills) == 0:
        skill_score = 0
    else:
        skill_score = (len(matched_skills) / len(jd_skills)) * 60

    # 2. Education Score - 15%
    education_score = 15 if education != "Not Found" else 0

    # 3. Projects Score - 15%
    projects_score = 15 if projects > 0 else 0

    # 4. Certifications Score - 10%
    certification_score = 10 if certifications > 0 else 0

    # Final ATS Score
    score = round(
        skill_score +
        education_score +
        projects_score +
        certification_score
    )

    # Keep score between 0 and 100
    score = min(score, 100)

        # Match classification
    if score >= 80:
        similarity = "High Match"
        suitability = "Excellent fit. Highly recommended."
    elif score >= 60:
        similarity = "Medium Match"
        suitability = "Good fit."
    elif score >= 40:
        similarity = "Low Match"
        suitability = "Needs Improvement."
    else:
        similarity = "Very Low Match"
        suitability = "Not recommended."


    # Suggestions
    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"Learn {skill}")


    # Interview Questions
    interview_questions = []

    question_bank = {
        "python": "Explain the difference between a list and a tuple in Python.",
        "java": "What is JVM and how does it work?",
        "sql": "What is the difference between INNER JOIN and LEFT JOIN?",
        "fastapi": "What are the advantages of FastAPI?",
        "docker": "What is Docker and why is it used?",
        "aws": "What is Amazon EC2?",
        "html": "What is the difference between HTML and HTML5?",
        "css": "What is Flexbox in CSS?",
        "javascript": "Explain the difference between var, let and const.",
        "git": "What is the difference between git merge and git rebase?"
    }

    for skill in missing_skills:
        if skill in question_bank:
            interview_questions.append(question_bank[skill])


    # Final Result
    return {
        "filename": filename,
        "category": category,
        "score": score,
        "similarity": similarity,
        "suitability": suitability,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "interview_questions": interview_questions,
        "candidate_name": candidate_name,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications
    }

@app.post("/analyze")
async def analyze(
    job_description: str = Form(...),
    category: str = Form(...),
    files: List[UploadFile] = File(...)
):
    start = time.time()

    contents = await asyncio.gather(*[file.read() for file in files])

    results = []

    for i, content in enumerate(contents):

        filename = files[i].filename.lower()

        if filename.endswith(".pdf"):
            reader = PdfReader(BytesIO(content))
            text = ""

            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
            print("PDF Text Length:", len(text))
            print(text[:500])

        else:
            text = content.decode(errors="ignore")

        result = generate_result(
            text,
            files[i].filename,
            job_description,
            category
        )

        results.append(result)

    results = [r for r in results if r is not None]
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    for i, r in enumerate(results):
        r["rank"] = i + 1

    # Generate latest PDF
    if results:
        generate_pdf(results[0], "candidate_report.pdf")
    else:
        return {
            "error": "No candidates were successfully analyzed.",
            "message": "Please check the resume analysis function."
        }
    print("PDF Generated")

    print("Time taken:", time.time() - start)

    return {"results": results}

from fastapi.responses import FileResponse

@app.get("/download-report")
def download_report():
    return FileResponse(
        "candidate_report.pdf",
        media_type="application/pdf",
        filename="candidate_report.pdf"
    )