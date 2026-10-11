import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.config import settings
from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import ResumeAnalysis
from app.models.skill import Skill, ResumeSkill
from app.schemas.resume import ResumeResponse, ResumeDetailResponse
from app.schemas.analysis import ResumeAnalysisResponse

from app.ai.text_extractor import extract_text_from_file
from app.ai.skill_extractor import extract_skills
from app.ai.resume_parser import parse_resume_sections
from app.ai.score_calculator import calculate_resume_score
from app.ai.llm_service import generate_ai_resume_feedback
from app.api.deps import get_current_user

router = APIRouter(prefix="/resumes", tags=["Resumes"])

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}

@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file extension '{file_ext}'. Only PDF (.pdf) and Word (.docx) documents are supported."
        )

    # Read bytes and check size
    contents = await file.read()
    file_size_mb = len(contents) / (1024 * 1024)
    if file_size_mb > settings.MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed limit of {settings.MAX_FILE_SIZE_MB}MB."
        )

    # Save to disk
    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
    saved_file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    with open(saved_file_path, "wb") as f:
        f.write(contents)

    # Extract text
    try:
        extracted_text, file_type = extract_text_from_file(saved_file_path, file.filename)
    except ValueError as val_err:
        if os.path.exists(saved_file_path):
            os.remove(saved_file_path)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(val_err))
    except Exception as err:
        if os.path.exists(saved_file_path):
            os.remove(saved_file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error reading document: {str(err)}"
        )

    # Save Resume Record
    resume = Resume(
        user_id=current_user.id,
        filename=file.filename,
        file_path=saved_file_path,
        file_type=file_type,
        extracted_text=extracted_text
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    # Trigger Automatic Analysis immediately upon upload
    _perform_resume_analysis(resume, current_user.id, db)

    return resume

@router.get("", response_model=List[ResumeResponse])
def get_user_resumes(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.uploaded_at.desc()).all()
    return resumes

@router.get("/{resume_id}", response_model=ResumeDetailResponse)
def get_resume_by_id(resume_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found or access denied.")
    return resume

@router.delete("/{resume_id}", status_code=status.HTTP_200_OK)
def delete_resume(resume_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found or access denied.")
    
    # Remove file from storage
    if os.path.exists(resume.file_path):
        try:
            os.remove(resume.file_path)
        except Exception:
            pass

    db.delete(resume)
    db.commit()
    return {"message": f"Resume '{resume.filename}' deleted successfully."}

@router.post("/{resume_id}/analyze", response_model=ResumeAnalysisResponse)
def trigger_analysis(resume_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found or access denied.")
    return _perform_resume_analysis(resume, current_user.id, db)

@router.get("/{resume_id}/analysis", response_model=ResumeAnalysisResponse)
def get_resume_analysis(resume_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    analysis = db.query(ResumeAnalysis).filter(ResumeAnalysis.resume_id == resume_id, ResumeAnalysis.user_id == current_user.id).first()
    if not analysis:
        # If not analyzed yet, run analysis
        resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
        if not resume:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")
        analysis = _perform_resume_analysis(resume, current_user.id, db)
    return analysis

def _perform_resume_analysis(resume: Resume, user_id: int, db: Session) -> ResumeAnalysis:
    text = resume.extracted_text or ""
    
    # 1. Skill Extraction
    skill_data = extract_skills(text)
    
    # 2. Section Parsing
    parsed_sections = parse_resume_sections(text)
    
    # 3. Score Calculation
    scores = calculate_resume_score(parsed_sections, skill_data, text)
    
    # 4. Optional LLM feedback enhancement
    llm_enhanced = generate_ai_resume_feedback(text, scores)
    suggestions = llm_enhanced.get("suggestions", scores.get("suggestions", []))

    # Clear previous analysis if re-analyzing
    existing_analysis = db.query(ResumeAnalysis).filter(ResumeAnalysis.resume_id == resume.id).first()
    if existing_analysis:
        db.delete(existing_analysis)
        db.commit()

    analysis = ResumeAnalysis(
        user_id=user_id,
        resume_id=resume.id,
        overall_score=scores["overall_score"],
        skills_score=scores["skills_score"],
        experience_score=scores["experience_score"],
        education_score=scores["education_score"],
        projects_score=scores["projects_score"],
        certifications_score=scores["certifications_score"],
        completeness_score=scores["completeness_score"],
        keyword_relevance_score=scores["keyword_relevance_score"],
        formatting_score=scores["formatting_score"],
        personal_info=parsed_sections["personal_info"],
        education=parsed_sections["education"],
        experience=parsed_sections["experience"],
        projects=parsed_sections["projects"],
        certifications=parsed_sections["certifications"],
        raw_extracted_data=skill_data,
        score_factors=scores["score_factors"],
        suggestions=suggestions
    )
    db.add(analysis)

    # Save Resume Skills
    db.query(ResumeSkill).filter(ResumeSkill.resume_id == resume.id).delete()
    for s_item in skill_data.get("skill_details", []):
        db_skill = db.query(Skill).filter(Skill.name == s_item["name"]).first()
        rs = ResumeSkill(
            resume_id=resume.id,
            skill_id=db_skill.id if db_skill else None,
            skill_name=s_item["name"],
            category=s_item["category"],
            confidence=s_item["confidence"]
        )
        db.add(rs)

    db.commit()
    db.refresh(analysis)
    return analysis
