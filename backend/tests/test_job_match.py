from app.ai.job_matcher import match_job_description

def test_job_matching_logic():
    resume_text = "Experienced Python developer with React, PostgreSQL, Docker, AWS and SQL background."
    candidate_skills = ["Python", "React", "PostgreSQL", "Docker", "AWS", "SQL"]
    
    job_title = "Senior Python Developer"
    job_description = "Looking for a Python Developer proficient in Python, SQL, PostgreSQL, Docker, and AWS."

    result = match_job_description(resume_text, candidate_skills, job_title, job_description)
    assert result["match_score"] >= 70.0
    assert "Python" in result["matching_skills"]
    assert "PostgreSQL" in result["matching_skills"]
