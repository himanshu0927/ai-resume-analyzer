from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.job import JobMatch
from app.schemas.job import JobMatchRequest, JobMatchResponse
from app.ai.job_matcher import match_job_description
from app.ai.skill_extractor import extract_skills
from app.api.deps import get_current_user

router = APIRouter(prefix="/job-match", tags=["Job Matcher"])

@router.post("", response_model=JobMatchResponse)
def match_job(payload: JobMatchRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Retrieve target resume or latest uploaded resume
    if payload.resume_id:
        resume = db.query(Resume).filter(Resume.id == payload.resume_id, Resume.user_id == current_user.id).first()
        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Specified resume not found.")
    else:
        resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.uploaded_at.desc()).first()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No resume uploaded yet. Please upload a resume first to run Job Matcher."
            )

    resume_text = resume.extracted_text or ""
    candidate_skills_data = extract_skills(resume_text)
    candidate_skills = candidate_skills_data.get("all_skills", [])

    match_result = match_job_description(
        resume_text=resume_text,
        candidate_skills=candidate_skills,
        job_title=payload.job_title,
        job_description=payload.job_description
    )

    # Save match in database
    job_match = JobMatch(
        user_id=current_user.id,
        resume_id=resume.id,
        job_title=payload.job_title,
        job_description=payload.job_description,
        match_score=match_result["match_score"],
        matching_skills=match_result["matching_skills"],
        missing_skills=match_result["missing_skills"],
        relevant_experience=match_result["relevant_experience"],
        relevant_projects=match_result["relevant_projects"],
        suggestions=match_result["suggestions"]
    )
    db.add(job_match)
    db.commit()
    db.refresh(job_match)

    return job_match

@router.get("/history", response_model=List[JobMatchResponse])
def get_job_match_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    matches = db.query(JobMatch).filter(JobMatch.user_id == current_user.id).order_by(JobMatch.created_at.desc()).all()
    return matches
