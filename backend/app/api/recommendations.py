from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.schemas.job import RecommendationResponse
from app.ai.recommendations import generate_job_recommendations
from app.ai.skill_extractor import extract_skills
from app.api.deps import get_current_user

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("", response_model=List[RecommendationResponse])
def get_recommendations(resume_id: Optional[int] = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if resume_id:
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    else:
        resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.uploaded_at.desc()).first()

    if not resume:
        return [
            RecommendationResponse(
                role="Full Stack Developer",
                match_percentage=75.0,
                reason="Upload your resume to get personalized role recommendations based on your detected technical skills.",
                key_matching_skills=["React", "Python", "SQL"]
            ),
            RecommendationResponse(
                role="Backend Developer",
                match_percentage=70.0,
                reason="Upload your resume to evaluate API & server-side development suitability.",
                key_matching_skills=["Python", "FastAPI", "Database"]
            )
        ]

    skills_data = extract_skills(resume.extracted_text or "")
    candidate_skills = skills_data.get("all_skills", [])
    
    recs = generate_job_recommendations(candidate_skills)
    return recs
