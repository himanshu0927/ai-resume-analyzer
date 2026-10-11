from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.analysis import ResumeAnalysis
from app.services.pdf_service import generate_resume_pdf_report
from app.api.deps import get_current_user

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/{resume_id}/pdf")
def download_resume_pdf_report(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found or access denied.")

    analysis = db.query(ResumeAnalysis).filter(ResumeAnalysis.resume_id == resume.id, ResumeAnalysis.user_id == current_user.id).first()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis report not found. Please analyze the resume first.")

    analysis_dict = {
        "overall_score": analysis.overall_score,
        "personal_info": analysis.personal_info or {},
        "score_factors": analysis.score_factors or [],
        "raw_extracted_data": analysis.raw_extracted_data or {},
        "suggestions": analysis.suggestions or []
    }

    pdf_bytes = generate_resume_pdf_report(analysis_dict, resume.filename)

    filename = f"Resume_Analysis_Report_{resume.id}.pdf"
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }

    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
