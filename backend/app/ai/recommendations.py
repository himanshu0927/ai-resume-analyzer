from typing import Dict, List, Any

TARGET_ROLES_REQUIREMENTS = {
    "Full Stack Developer": {
        "core_skills": ["React", "Node.js", "JavaScript", "TypeScript", "Python", "SQL", "HTML", "CSS", "REST API", "Git"],
        "min_match": 3
    },
    "Frontend Developer": {
        "core_skills": ["React", "Angular", "Vue", "JavaScript", "TypeScript", "HTML", "CSS", "Tailwind", "Redux", "Vite"],
        "min_match": 2
    },
    "Backend Developer": {
        "core_skills": ["Python", "FastAPI", "Django", "Node.js", "Java", "Express", "SQL", "PostgreSQL", "MongoDB", "REST API"],
        "min_match": 3
    },
    "Python Developer": {
        "core_skills": ["Python", "Django", "FastAPI", "Flask", "SQL", "PostgreSQL", "Git", "REST API"],
        "min_match": 2
    },
    "Data Scientist": {
        "core_skills": ["Python", "R", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "SQL", "Machine Learning"],
        "min_match": 3
    },
    "Machine Learning Engineer": {
        "core_skills": ["Python", "PyTorch", "TensorFlow", "Scikit-learn", "Machine Learning", "Deep Learning", "NLP", "Docker"],
        "min_match": 3
    },
    "Data Analyst": {
        "core_skills": ["Python", "SQL", "Pandas", "Power BI", "Tableau", "Excel", "Data Analysis", "Data Visualization"],
        "min_match": 2
    },
    "DevOps Engineer": {
        "core_skills": ["Docker", "Kubernetes", "Linux", "AWS", "CI/CD", "Git", "Jenkins", "Terraform", "Nginx"],
        "min_match": 2
    },
    "Cloud Engineer": {
        "core_skills": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Linux", "Terraform", "Serverless"],
        "min_match": 2
    }
}

def generate_job_recommendations(candidate_skills: List[str]) -> List[Dict[str, Any]]:
    """
    Generates recommended job roles based on candidate technical skills.
    Includes explicit reason string: 'Recommended because your resume contains Python, SQL, Pandas...'
    """
    candidate_set = set([s.lower() for s in candidate_skills])
    recommendations = []

    for role, data in TARGET_ROLES_REQUIREMENTS.items():
        req_skills = data["core_skills"]
        matching = [s for s in req_skills if s.lower() in candidate_set]
        
        if len(matching) >= data["min_match"]:
            match_percentage = min(95.0, round((len(matching) / max(4, len(req_skills))) * 100, 1))
            reason = f"Recommended because your resume contains {', '.join(matching[:4])}."
            
            recommendations.append({
                "role": role,
                "match_percentage": max(50.0, match_percentage),
                "reason": reason,
                "key_matching_skills": matching
            })

    # Sort by highest match percentage
    recommendations.sort(key=lambda x: x["match_percentage"], reverse=True)

    # Fallback recommendations if candidate skills are low
    if not recommendations:
        recommendations = [
            {
                "role": "Full Stack Developer",
                "match_percentage": 65.0,
                "reason": "Recommended based on core programming skills and web application background.",
                "key_matching_skills": candidate_skills[:3] if candidate_skills else ["Programming", "Web Basics"]
            },
            {
                "role": "Python Developer",
                "match_percentage": 60.0,
                "reason": "Recommended based on general technical and software logic capabilities.",
                "key_matching_skills": candidate_skills[:2] if candidate_skills else ["Problem Solving"]
            }
        ]

    return recommendations[:6]
