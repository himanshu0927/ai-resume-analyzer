from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.schemas.job import SkillGapResponse
from app.ai.skill_gap_analyzer import analyze_skill_gap
from app.ai.skill_extractor import extract_skills
from app.api.deps import get_current_user

router = APIRouter(prefix="/skill-gap", tags=["Skill Gap"])

@router.get("", response_model=SkillGapResponse)
def get_skill_gap_analysis(
    target_role: str = Query("Full Stack Developer"),
    resume_id: Optional[int] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if resume_id:
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    else:
        resume = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.uploaded_at.desc()).first()

    if resume:
        skills_data = extract_skills(resume.extracted_text or "")
        candidate_skills = skills_data.get("all_skills", [])
    else:
        candidate_skills = []

    analysis = analyze_skill_gap(candidate_skills, target_role)
    return analysis
