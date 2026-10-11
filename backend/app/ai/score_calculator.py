from typing import Dict, List, Any

def calculate_resume_score(parsed_data: Dict[str, Any], skill_data: Dict[str, Any], raw_text: str) -> Dict[str, Any]:
    """
    Calculates a transparent multi-factor Resume Analysis Score (0-100).
    Components:
    - Skills score (weight: 25%)
    - Experience score (weight: 20%)
    - Projects score (weight: 20%)
    - Education score (weight: 15%)
    - Certifications score (weight: 5%)
    - Profile completeness score (weight: 5%)
    - Keyword relevance score (weight: 5%)
    - Formatting & readability score (weight: 5%)
    """
    all_skills = skill_data.get("all_skills", [])
    categorized = skill_data.get("categorized_skills", {})
    
    # 1. Skills Score (0-100)
    skills_count = len(all_skills)
    categories_present = sum(1 for cat, s_list in categorized.items() if len(s_list) > 0)
    
    if skills_count >= 15:
        skills_score = 95.0
    elif skills_count >= 10:
        skills_score = 85.0
    elif skills_count >= 5:
        skills_score = 70.0
    elif skills_count >= 2:
        skills_score = 50.0
    else:
        skills_score = 25.0
    # Bonus for category breadth
    skills_score = min(100.0, skills_score + (categories_present * 1.5))

    # 2. Experience Score (0-100)
    experiences = parsed_data.get("experience", [])
    if len(experiences) >= 3:
        experience_score = 90.0
    elif len(experiences) == 2:
        experience_score = 80.0
    elif len(experiences) == 1:
        experience_score = 65.0
    else:
        experience_score = 40.0

    # 3. Projects Score (0-100)
    projects = parsed_data.get("projects", [])
    if len(projects) >= 3:
        projects_score = 95.0
    elif len(projects) == 2:
        projects_score = 85.0
    elif len(projects) == 1:
        projects_score = 70.0
    else:
        projects_score = 35.0

    # 4. Education Score (0-100)
    education = parsed_data.get("education", [])
    if len(education) >= 1 and any("B." in e.get("degree", "") or "M." in e.get("degree", "") or "Bachelor" in e.get("degree", "") for e in education):
        education_score = 90.0
    elif len(education) >= 1:
        education_score = 75.0
    else:
        education_score = 50.0

    # 5. Certifications Score (0-100)
    certs = parsed_data.get("certifications", [])
    if len(certs) >= 3:
        certifications_score = 95.0
    elif len(certs) == 2:
        certifications_score = 85.0
    elif len(certs) == 1:
        certifications_score = 70.0
    else:
        certifications_score = 30.0

    # 6. Profile Completeness Score (0-100)
    p_info = parsed_data.get("personal_info", {})
    completeness_items = [
        bool(p_info.get("name") and p_info.get("name") != "Candidate"),
        bool(p_info.get("email") and "@" in p_info.get("email")),
        bool(p_info.get("phone") and p_info.get("phone") != "Not provided"),
        bool(p_info.get("location") and p_info.get("location") != "Not specified"),
        bool(parsed_data.get("summary")),
        bool(education),
        bool(projects),
        bool(all_skills)
    ]
    completeness_score = (sum(completeness_items) / len(completeness_items)) * 100.0

    # 7. Keyword Relevance Score (0-100)
    action_verbs = ["developed", "built", "implemented", "designed", "created", "managed", "analyzed", "architected", "optimized", "led"]
    verb_count = sum(1 for v in action_verbs if v in raw_text.lower())
    keyword_relevance_score = min(100.0, (verb_count / len(action_verbs)) * 100.0 + 30.0)

    # 8. Formatting Score (0-100)
    text_length = len(raw_text)
    if 1000 <= text_length <= 5000:
        formatting_score = 90.0
    elif 500 <= text_length < 1000:
        formatting_score = 75.0
    else:
        formatting_score = 60.0

    # Weighted Overall Score
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

    # Contributing factors summary for display
    score_factors = [
        {"factor": "Technical Skills Depth", "weight": "25%", "score": round(skills_score, 1), "status": "Good" if skills_score >= 70 else "Needs Improvement"},
        {"factor": "Practical Projects", "weight": "20%", "score": round(projects_score, 1), "status": "Good" if projects_score >= 70 else "Needs Improvement"},
        {"factor": "Work Experience", "weight": "20%", "score": round(experience_score, 1), "status": "Good" if experience_score >= 70 else "Needs Improvement"},
        {"factor": "Academic Background", "weight": "15%", "score": round(education_score, 1), "status": "Good" if education_score >= 70 else "Needs Improvement"},
        {"factor": "Certifications & Badges", "weight": "5%", "score": round(certifications_score, 1), "status": "Good" if certifications_score >= 70 else "Needs Improvement"},
        {"factor": "Profile Completeness", "weight": "5%", "score": round(completeness_score, 1), "status": "Good" if completeness_score >= 70 else "Needs Improvement"},
        {"factor": "Keyword & Action Verbs", "weight": "5%", "score": round(keyword_relevance_score, 1), "status": "Good" if keyword_relevance_score >= 70 else "Needs Improvement"},
        {"factor": "Formatting & Length", "weight": "5%", "score": round(formatting_score, 1), "status": "Good" if formatting_score >= 70 else "Needs Improvement"}
    ]

    # Prioritized Improvement Suggestions
    suggestions = []
    if skills_count < 8:
        suggestions.append({
            "priority": "High",
            "category": "Skills",
            "text": "Add 4–6 key technical skills (e.g. Docker, PostgreSQL, React, AWS) to improve ATS keyword visibility."
        })
    if len(projects) < 2:
        suggestions.append({
            "priority": "High",
            "category": "Projects",
            "text": "Detail at least 2 full-stack or AI-driven projects with metrics and tech stack used."
        })
    if verb_count < 4:
        suggestions.append({
            "priority": "Medium",
            "category": "Keywords",
            "text": "Use strong action verbs like 'Designed', 'Architected', 'Optimized', and 'Deployed' at the start of bullet points."
        })
    if len(certs) == 0:
        suggestions.append({
            "priority": "Low",
            "category": "Certifications",
            "text": "Include professional certifications or specialized online course certificates (e.g. AWS, Coursera, Meta)."
        })
    if not parsed_data.get("summary"):
        suggestions.append({
            "priority": "Medium",
            "category": "Summary",
            "text": "Add a compelling 2–3 sentence professional summary at the top of your resume outlining your core tech stack and career goal."
        })

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
