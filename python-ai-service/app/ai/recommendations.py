from typing import Dict, List, Any

TARGET_ROLES = {
    "Full Stack Developer": ["React", "Node.js", "JavaScript", "Python", "SQL", "Java", "HTML", "CSS"],
    "Backend Developer": ["Python", "Java", "FastAPI", "Spring Boot", "SQL", "PostgreSQL", "Docker"],
    "Frontend Developer": ["JavaScript", "TypeScript", "React", "HTML", "CSS", "Tailwind"],
    "Python Developer": ["Python", "FastAPI", "Django", "SQL", "Git"],
    "Java Developer": ["Java", "Spring Boot", "SQL", "PostgreSQL", "Git", "REST API"],
    "Data Scientist": ["Python", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "SQL", "Machine Learning"],
    "Machine Learning Engineer": ["Python", "PyTorch", "TensorFlow", "Machine Learning", "Deep Learning", "Docker"],
    "DevOps Engineer": ["Docker", "Kubernetes", "Linux", "AWS", "CI/CD", "Git"]
}

def generate_job_recommendations(candidate_skills: List[str]) -> List[Dict[str, Any]]:
    candidate_set = set([s.lower() for s in candidate_skills])
    recommendations = []

    for role, req_skills in TARGET_ROLES.items():
        matching = [s for s in req_skills if s.lower() in candidate_set]
        if len(matching) >= 2 or not candidate_skills:
            match_percentage = min(95.0, round((len(matching) / max(3, len(req_skills))) * 100, 1))
            reason = f"Recommended because your resume contains {', '.join(matching[:4])}." if matching else "Recommended based on core technical background."
            recommendations.append({
                "role": role,
                "match_percentage": max(55.0, match_percentage),
                "reason": reason,
                "key_matching_skills": matching or ["Programming Basics"]
            })

    recommendations.sort(key=lambda x: x["match_percentage"], reverse=True)
    return recommendations[:6]
