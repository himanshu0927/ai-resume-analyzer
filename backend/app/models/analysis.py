import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    overall_score = Column(Float, nullable=False, default=0.0)
    skills_score = Column(Float, nullable=False, default=0.0)
    experience_score = Column(Float, nullable=False, default=0.0)
    education_score = Column(Float, nullable=False, default=0.0)
    projects_score = Column(Float, nullable=False, default=0.0)
    certifications_score = Column(Float, nullable=False, default=0.0)
    completeness_score = Column(Float, nullable=False, default=0.0)
    keyword_relevance_score = Column(Float, nullable=False, default=0.0)
    formatting_score = Column(Float, nullable=False, default=0.0)

    personal_info = Column(JSON, nullable=True)
    education = Column(JSON, nullable=True)
    experience = Column(JSON, nullable=True)
    projects = Column(JSON, nullable=True)
    certifications = Column(JSON, nullable=True)
    raw_extracted_data = Column(JSON, nullable=True)
    score_factors = Column(JSON, nullable=True)
    suggestions = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="analyses")
    resume = relationship("Resume", back_populates="analysis")
