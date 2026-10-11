from typing import Dict, List, Any
from app.ai.recommendations import TARGET_ROLES_REQUIREMENTS

ROLE_PROJECT_IDEAS = {
    "Full Stack Developer": [
        "Build a Real-Time Collaborative Dashboard using React, FastAPI, WebSockets, and PostgreSQL.",
        "Develop an E-Commerce API with JWT authentication, Stripe integration, and Docker containerization."
    ],
    "Frontend Developer": [
        "Create an Interactive Data Visualization SaaS Interface with React, TypeScript, and Tailwind CSS.",
        "Build a Micro-Frontend Dashboard supporting dynamic theme customization and skeleton loaders."
    ],
    "Backend Developer": [
        "Architect a High-Throughput REST & GraphQL Service using FastAPI, SQLAlchemy, Redis caching, and Pytest.",
        "Build an Asynchronous Background Job Processing Pipeline with Celery and PostgreSQL."
    ],
    "Data Scientist": [
        "Predict Customer Churn using Scikit-Learn, Pandas, and deployed ML model via FastAPI endpoint.",
        "Build an End-to-End Sentiment Analysis Pipeline with Hugging Face Transformers and Streamlit."
    ],
    "Machine Learning Engineer": [
        "Deploy a Computer Vision Model using PyTorch and Docker to AWS ECS with CI/CD GitHub Actions.",
        "Build a Retrieval-Augmented Generation (RAG) System using LangChain, Vector Database, and LlamaIndex."
    ],
    "DevOps Engineer": [
        "Build an Automated Kubernetes Deployment Pipeline using Helm, ArgoCD, and GitHub Actions.",
        "Provision a Multi-Region Cloud Infrastructure using Terraform and Ansible."
    ]
}

def analyze_skill_gap(candidate_skills: List[str], target_role: str) -> Dict[str, Any]:
    """
    Compares candidate skills against target role skills.
    Categorizes into: Already Learned, Partially Covered, Missing.
    Provides targeted learning topics and project suggestions.
    """
    candidate_set = set([s.lower() for s in candidate_skills])
    
    role_info = TARGET_ROLES_REQUIREMENTS.get(target_role)
    if not role_info:
        # Default to Full Stack Developer target skills if unknown role
        target_role = "Full Stack Developer"
        role_info = TARGET_ROLES_REQUIREMENTS["Full Stack Developer"]

    target_skills = role_info["core_skills"]

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

    total_target = len(target_skills)
    learned_pct = round((len(already_learned) / max(1, total_target)) * 100, 1)
    partial_pct = round((len(partially_covered) / max(1, total_target)) * 100, 1)
    missing_pct = round((len(missing) / max(1, total_target)) * 100, 1)

    topics_to_learn = [f"Deep dive into {s} fundamentals & hands-on application" for s in missing[:4]]
    if not topics_to_learn:
        topics_to_learn = ["Advanced System Design", "Microservices Architecture", "Performance Optimization"]

    suggested_projects = ROLE_PROJECT_IDEAS.get(target_role, [
        f"Build a production-style {target_role} portfolio project integrating missing skills: {', '.join(missing[:3])}."
    ])

    practice_areas = [
        "Solve algorithmic coding challenges on LeetCode / HackerRank",
        f"Build end-to-end CRUD features showcasing {missing[0] if missing else 'System Design'}",
        "Configure automated CI/CD unit testing and deployment scripts"
    ]

    return {
        "target_role": target_role,
        "total_target_skills": total_target,
        "already_learned": already_learned,
        "partially_covered": partially_covered,
        "missing": missing,
        "stats": {
            "learned_count": len(already_learned),
            "learned_percentage": learned_pct,
            "partial_count": len(partially_covered),
            "partial_percentage": partial_pct,
            "missing_count": len(missing),
            "missing_percentage": missing_pct
        },
        "learning_suggestions": {
            "topics_to_learn": topics_to_learn,
            "suggested_project_ideas": suggested_projects,
            "suggested_practice_areas": practice_areas
        }
    }
