from app.ai.skill_extractor import extract_skills
from app.ai.resume_parser import parse_resume_sections
from app.ai.score_calculator import calculate_resume_score

SAMPLE_RESUME = """
Jane Doe
Email: jane.doe@example.com
Phone: +1 555-0199
Location: San Francisco, CA

SUMMARY
Enthusiastic Software Engineer with 3+ years experience in Full Stack Web Development and AI.

SKILLS
Programming: Python, JavaScript, TypeScript, SQL
Web: React, FastAPI, Node.js, HTML, CSS, Tailwind
Database & Cloud: PostgreSQL, MongoDB, Docker, AWS, Git

EXPERIENCE
Software Engineer | TechCorp Inc
Jan 2022 - Present
- Architected microservices with Python, FastAPI, and PostgreSQL.
- Implemented real-time dashboard components in React and TypeScript.

EDUCATION
B.Tech in Computer Science
State Tech University, 2021

PROJECTS
AI Resume Analyzer
Built a full-stack web application using FastAPI, React, and PostgreSQL for resume scoring.
"""

def test_skill_extraction():
    skills = extract_skills(SAMPLE_RESUME)
    extracted_names = skills["all_skills"]
    assert "Python" in extracted_names
    assert "React" in extracted_names
    assert "FastAPI" in extracted_names
    assert "PostgreSQL" in extracted_names
    assert "Docker" in extracted_names

def test_resume_parser():
    parsed = parse_resume_sections(SAMPLE_RESUME)
    assert parsed["personal_info"]["email"] == "jane.doe@example.com"
    assert len(parsed["education"]) >= 1
    assert len(parsed["experience"]) >= 1

def test_score_calculation():
    skills = extract_skills(SAMPLE_RESUME)
    parsed = parse_resume_sections(SAMPLE_RESUME)
    scores = calculate_resume_score(parsed, skills, SAMPLE_RESUME)
    assert 0 <= scores["overall_score"] <= 100
    assert scores["skills_score"] > 50
