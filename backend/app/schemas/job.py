import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class JobMatchRequest(BaseModel):
    resume_id: Optional[int] = None
    job_title: str = Field(..., min_length=2, max_length=200)
    job_description: str = Field(..., min_length=10)

class JobMatchResponse(BaseModel):
    id: Optional[int] = None
    resume_id: Optional[int] = None
    job_title: str
    job_description: str
    match_score: float
    matching_skills: List[str]
    missing_skills: List[str]
    relevant_experience: List[str]
    relevant_projects: List[str]
    suggestions: List[Dict[str, Any]]
    created_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

class RecommendationResponse(BaseModel):
    id: Optional[int] = None
    role: str
    match_percentage: float
    reason: str
    key_matching_skills: List[str]

    class Config:
        from_attributes = True

class SkillGapRequest(BaseModel):
    resume_id: Optional[int] = None
    target_role: str = "Full Stack Developer"

class SkillGapResponse(BaseModel):
    target_role: str
    total_target_skills: int
    already_learned: List[str]
    partially_covered: List[str]
    missing: List[str]
    stats: Dict[str, Any]
    learning_suggestions: Dict[str, Any]
