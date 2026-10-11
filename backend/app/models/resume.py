import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=False)
    extracted_text = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="resumes")
    analysis = relationship("ResumeAnalysis", back_populates="resume", uselist=False, cascade="all, delete-orphan")
    skills = relationship("ResumeSkill", back_populates="resume", cascade="all, delete-orphan")
    job_matches = relationship("JobMatch", back_populates="resume", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="resume", cascade="all, delete-orphan")
