import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from app.config import settings
from app.ai.text_extractor import extract_text_from_file
from app.ai.skill_extractor import extract_skills
from app.ai.resume_parser import parse_resume_sections
from app.ai.score_calculator import calculate_resume_score
from app.ai.job_matcher import match_job_description
from app.ai.recommendations import generate_job_recommendations
from app.ai.skill_gap_analyzer import analyze_skill_gap
from app.ai.pdf_service import generate_pdf_report

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Python AI & NLP Microservice for Resume Scoring & Job Matching",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobMatchPayload(BaseModel):
    resume_text: str
    candidate_skills: List[str]
    job_title: str
    job_description: str

class SkillGapPayload(BaseModel):
    candidate_skills: List[str]
    target_role: str = "Full Stack Developer"

@app.get("/")
def root():
    return {"service": "Python AI & NLP Microservice", "status": "online"}

@app.post("/api/ai/parse-resume")
async def parse_resume_endpoint(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".docx", ".doc"]:
        raise HTTPException(status_code=400, detail=f"Unsupported format '{ext}'. Upload PDF or DOCX.")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 10MB limit.")

    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    saved_path = os.path.join(settings.UPLOAD_DIR, unique_name)
    with open(saved_path, "wb") as f:
        f.write(contents)

    try:
        raw_text, file_type = extract_text_from_file(saved_path, file.filename)
        skill_data = extract_skills(raw_text)
        parsed_sections = parse_resume_sections(raw_text)
        score_data = calculate_resume_score(parsed_sections, skill_data, raw_text)
        recommendations = generate_job_recommendations(skill_data["all_skills"])

        return {
            "filename": file.filename,
            "file_type": file_type,
            "extracted_text": raw_text,
            "skills": skill_data,
            "sections": parsed_sections,
            "scores": score_data,
            "recommendations": recommendations
        }
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

@app.post("/api/ai/match-job")
def match_job_endpoint(payload: JobMatchPayload):
    result = match_job_description(
        resume_text=payload.resume_text,
        candidate_skills=payload.candidate_skills,
        job_title=payload.job_title,
        job_description=payload.job_description
    )
    return result

@app.post("/api/ai/skill-gap")
def skill_gap_endpoint(payload: SkillGapPayload):
    result = analyze_skill_gap(payload.candidate_skills, payload.target_role)
    return result

@app.post("/api/ai/pdf-report")
def pdf_report_endpoint(analysis_data: dict):
    pdf_bytes = generate_pdf_report(analysis_data, analysis_data.get("filename", "Resume_Analysis.pdf"))
    headers = {'Content-Disposition': 'attachment; filename="Resume_Analysis_Report.pdf"'}
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
