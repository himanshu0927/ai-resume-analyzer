import re
from typing import Dict, List, Any
from app.ai.skill_extractor import extract_skills

def match_job_description(resume_text: str, candidate_skills: List[str], job_title: str, job_description: str) -> Dict[str, Any]:
    """
    Compares candidate resume against job title and job description.
    Returns:
    - match_score (%)
    - matching_skills
    - missing_skills
    - relevant_experience
    - relevant_projects
    - suggestions
    """
    # Extract required skills from job description
    job_skill_data = extract_skills(job_description + " " + job_title)
    job_required_skills = job_skill_data.get("all_skills", [])
    
    # If job description didn't yield skills from taxonomy, fall back to basic token extraction
    if not job_required_skills:
        words = re.findall(r'\b[A-Za-z]{3,}\b', job_description)
        job_required_skills = list(set([w.title() for w in words[:10]]))

    candidate_skills_set = set([s.lower() for s in candidate_skills])
    
    matching_skills = []
    missing_skills = []
    
    for skill in job_required_skills:
        if skill.lower() in candidate_skills_set:
            matching_skills.append(skill)
        else:
            missing_skills.append(skill)

    # Calculate skill match ratio
    if job_required_skills:
        skill_match_ratio = len(matching_skills) / len(job_required_skills)
    else:
        skill_match_ratio = 0.5

    # Text overlap / keyword coverage ratio
    job_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', job_description.lower()))
    resume_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', resume_text.lower()))
    
    keyword_overlap = len(job_words.intersection(resume_words)) / max(1, len(job_words))
    
    # Overall Job Match Score calculation
    raw_match_score = (skill_match_ratio * 70.0) + (keyword_overlap * 30.0)
    match_score = round(min(98.0, max(15.0, raw_match_score * 100 if raw_match_score <= 1 else raw_match_score)), 1)

    # Identify relevant experience bullet points matching job keywords
    relevant_experience = []
    lines = resume_text.split('\n')
    for line in lines:
        if len(line.strip()) > 25:
            overlap = set(re.findall(r'\b[a-zA-Z]{4,}\b', line.lower())).intersection(job_words)
            if len(overlap) >= 3:
                relevant_experience.append(line.strip())
                if len(relevant_experience) >= 3:
                    break

    # Improvement Suggestions
    suggestions = []
    if missing_skills:
        top_missing = missing_skills[:4]
        suggestions.append({
            "type": "Skill Gap",
            "text": f"Add experience or projects demonstrating key target skills: {', '.join(top_missing)}."
        })
    if match_score < 70:
        suggestions.append({
            "type": "Keyword Optimization",
            "text": f"Incorporate industry terminology from the '{job_title}' job description into your summary and project descriptions."
        })
    suggestions.append({
        "type": "Quantifiable Metrics",
        "text": "Highlight measurable metrics (e.g. 'Improved speed by 30%', 'Served 10k users') in your responsibilities."
    })

    return {
        "job_title": job_title,
        "match_score": match_score,
        "matching_skills": sorted(matching_skills),
        "missing_skills": sorted(missing_skills),
        "keyword_coverage_percent": round(keyword_overlap * 100, 1),
        "relevant_experience": relevant_experience or ["Relevant technical project work matching role requirements."],
        "relevant_projects": [f"Projects featuring {', '.join(matching_skills[:3])}"] if matching_skills else ["General Technical Project"],
        "suggestions": suggestions
    }
