import datetime
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ResumeAnalysisResponse(BaseModel):
    id: int
    user_id: int
    resume_id: int
    
    overall_score: float
    skills_score: float
    experience_score: float
    education_score: float
    projects_score: float
    certifications_score: float
    completeness_score: float
    keyword_relevance_score: float
    formatting_score: float

    personal_info: Optional[Dict[str, Any]] = None
    education: Optional[List[Dict[str, Any]]] = None
    experience: Optional[List[Dict[str, Any]]] = None
    projects: Optional[List[Dict[str, Any]]] = None
    certifications: Optional[List[str]] = None
    raw_extracted_data: Optional[Dict[str, Any]] = None
    score_factors: Optional[List[Dict[str, Any]]] = None
    suggestions: Optional[List[Dict[str, Any]]] = None
    
    created_at: datetime.datetime

    class Config:
        from_attributes = True
