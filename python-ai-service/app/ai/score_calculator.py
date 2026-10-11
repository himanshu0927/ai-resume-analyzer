from typing import Dict, List, Any

def calculate_resume_score(parsed_data: Dict[str, Any], skill_data: Dict[str, Any], raw_text: str) -> Dict[str, Any]:
    all_skills = skill_data.get("all_skills", [])
    categorized = skill_data.get("categorized_skills", {})
    
    skills_count = len(all_skills)
    categories_present = sum(1 for cat, s_list in categorized.items() if len(s_list) > 0)
    
    skills_score = min(100.0, 30.0 + (skills_count * 4.5) + (categories_present * 2.0))
    experience_score = min(100.0, 50.0 + len(parsed_data.get("experience", [])) * 20.0)
    projects_score = min(100.0, 50.0 + len(parsed_data.get("projects", [])) * 15.0)
    education_score = 90.0 if parsed_data.get("education") else 60.0
    certifications_score = min(100.0, 40.0 + len(parsed_data.get("certifications", [])) * 25.0)
    completeness_score = 85.0
    keyword_relevance_score = 80.0
    formatting_score = 85.0

    overall_score = (
        (skills_score * 0.25) +
        (experience_score * 0.20) +
        (projects_score * 0.20) +
        (education_score * 0.15) +
        (certifications_score * 0.05) +
        (completeness_score * 0.05) +
        (keyword_relevance_score * 0.05) +
        (formatting_score * 0.05)
    )
    overall_score = round(min(100.0, max(0.0, overall_score)), 1)

    score_factors = [
        {"factor": "Technical Skills Depth", "weight": "25%", "score": round(skills_score, 1), "status": "Good" if skills_score >= 70 else "Needs Improvement"},
        {"factor": "Practical Projects", "weight": "20%", "score": round(projects_score, 1), "status": "Good" if projects_score >= 70 else "Needs Improvement"},
        {"factor": "Work Experience", "weight": "20%", "score": round(experience_score, 1), "status": "Good" if experience_score >= 70 else "Needs Improvement"},
        {"factor": "Academic Background", "weight": "15%", "score": round(education_score, 1), "status": "Good" if education_score >= 70 else "Needs Improvement"},
        {"factor": "Certifications & Badges", "weight": "5%", "score": round(certifications_score, 1), "status": "Good" if certifications_score >= 70 else "Needs Improvement"},
        {"factor": "Profile Completeness", "weight": "5%", "score": round(completeness_score, 1), "status": "Good"},
        {"factor": "Keyword Relevance", "weight": "5%", "score": round(keyword_relevance_score, 1), "status": "Good"},
        {"factor": "Formatting & Layout", "weight": "5%", "score": round(formatting_score, 1), "status": "Good"}
    ]

    suggestions = []
    if skills_count < 8:
        suggestions.append({"priority": "High", "category": "Skills", "text": "Add 4–6 technical skills (e.g. Python, Java, Docker, React) to boost ATS index score."})
    if len(parsed_data.get("projects", [])) < 2:
        suggestions.append({"priority": "High", "category": "Projects", "text": "Detail at least 2 full-stack or AI projects with metrics and tech stack."})
    suggestions.append({"priority": "Medium", "category": "Action Verbs", "text": "Use strong action verbs like 'Designed', 'Architected', and 'Deployed'."})

    return {
        "overall_score": overall_score,
        "skills_score": round(skills_score, 1),
        "experience_score": round(experience_score, 1),
        "education_score": round(education_score, 1),
        "projects_score": round(projects_score, 1),
        "certifications_score": round(certifications_score, 1),
        "completeness_score": round(completeness_score, 1),
        "keyword_relevance_score": round(keyword_relevance_score, 1),
        "formatting_score": round(formatting_score, 1),
        "score_factors": score_factors,
        "suggestions": suggestions
    }
