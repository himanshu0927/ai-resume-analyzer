import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    company = Column(String(200), nullable=False)
    location = Column(String(200), nullable=True)
    description = Column(Text, nullable=False)
    required_skills = Column(JSON, nullable=True)
    experience_level = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    job_matches = relationship("JobMatch", back_populates="job", cascade="all, delete-orphan")

class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    
    job_title = Column(String(200), nullable=False)
    job_description = Column(Text, nullable=False)
    match_score = Column(Float, nullable=False, default=0.0)
    
    matching_skills = Column(JSON, nullable=True)
    missing_skills = Column(JSON, nullable=True)
    relevant_experience = Column(JSON, nullable=True)
    relevant_projects = Column(JSON, nullable=True)
    suggestions = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="job_matches")
    resume = relationship("Resume", back_populates="job_matches")
    job = relationship("Job", back_populates="job_matches")

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    role = Column(String(150), nullable=False)
    match_percentage = Column(Float, nullable=False, default=0.0)
    reason = Column(Text, nullable=False)
    key_matching_skills = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="recommendations")
    resume = relationship("Resume", back_populates="recommendations")
