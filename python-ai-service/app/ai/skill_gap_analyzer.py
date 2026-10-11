from typing import Dict, List, Any
from app.ai.recommendations import TARGET_ROLES

def analyze_skill_gap(candidate_skills: List[str], target_role: str) -> Dict[str, Any]:
    candidate_set = set([s.lower() for s in candidate_skills])
    target_skills = TARGET_ROLES.get(target_role, TARGET_ROLES["Full Stack Developer"])

    already_learned = []
    partially_covered = []
    missing = []

    for skill in target_skills:
        skill_lower = skill.lower()
        if skill_lower in candidate_set:
            already_learned.append(skill)
        elif any(skill_lower in s.lower() or s.lower() in skill_lower for s in candidate_set):
            partially_covered.append(skill)
        else:
            missing.append(skill)

    total = len(target_skills)
    return {
        "target_role": target_role,
        "total_target_skills": total,
        "already_learned": already_learned,
        "partially_covered": partially_covered,
        "missing": missing,
        "stats": {
            "learned_count": len(already_learned),
            "learned_percentage": round((len(already_learned)/max(1, total))*100, 1),
            "partial_count": len(partially_covered),
            "partial_percentage": round((len(partially_covered)/max(1, total))*100, 1),
            "missing_count": len(missing),
            "missing_percentage": round((len(missing)/max(1, total))*100, 1)
        },
        "learning_suggestions": {
            "topics_to_learn": [f"Master {s} fundamentals & core application" for s in missing[:4]] or ["System Architecture & Optimization"],
            "suggested_project_ideas": [f"Build a portfolio web app integrating {', '.join(missing[:3]) if missing else 'microservices'}."],
            "suggested_practice_areas": ["Data Structures & Algorithms", "Clean Code Principles", "Automated Testing"]
        }
    }
