from app.ai.skill_extractor import extract_skills
from app.ai.resume_parser import parse_resume_sections
from app.ai.score_calculator import calculate_resume_score
from app.ai.job_matcher import match_job_description

SAMPLE = """
Alex Johnson
Email: alex@example.com
Phone: +1 555-0199
Skills: Python, Java, JavaScript, React, SQL, PostgreSQL, Docker, AWS
Experience: Software Developer at Tech Inc (2022-Present)
Education: B.Tech in Computer Science (2021)
Projects: Built AI Resume Matcher using Python and Java
"""

def test_python_ai_pipeline():
    skills = extract_skills(SAMPLE)
    assert "Python" in skills["all_skills"]
    assert "Java" in skills["all_skills"]
    assert "React" in skills["all_skills"]

    parsed = parse_resume_sections(SAMPLE)
    assert parsed["personal_info"]["email"] == "alex@example.com"

    scores = calculate_resume_score(parsed, skills, SAMPLE)
    assert 0 <= scores["overall_score"] <= 100

    match = match_job_description(SAMPLE, skills["all_skills"], "Java Engineer", "Looking for Java, Python, SQL developer")
    assert match["match_score"] >= 60.0
