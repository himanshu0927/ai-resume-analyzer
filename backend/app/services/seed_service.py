from sqlalchemy.orm import Session
from app.models.skill import Skill
from app.models.job import Job
from app.ai.skill_taxonomy import SKILL_TAXONOMY

SAMPLE_JOBS = [
    {
        "title": "Full Stack Software Engineer",
        "company": "TechCorp Innovations",
        "location": "Remote / San Francisco, CA",
        "description": "We are seeking a skilled Full Stack Engineer proficient in React, TypeScript, Python, FastAPI, and PostgreSQL. You will design, build, and deploy scalable cloud applications, implement RESTful microservices, and optimize frontend user interfaces.",
        "required_skills": ["React", "TypeScript", "Python", "FastAPI", "PostgreSQL", "Docker", "Git", "REST API"],
        "experience_level": "Mid-Senior"
    },
    {
        "title": "Backend Python Engineer",
        "company": "DataCloud Solutions",
        "location": "New York, NY (Hybrid)",
        "description": "Join our platform team to build high-performance data pipelines and microservices. Required skills: Python, Django, FastAPI, PostgreSQL, Redis, Docker, and AWS.",
        "required_skills": ["Python", "FastAPI", "Django", "PostgreSQL", "Redis", "Docker", "AWS", "Git"],
        "experience_level": "Entry-Mid"
    },
    {
        "title": "Frontend React Developer",
        "company": "PixelCraft UI Lab",
        "location": "Austin, TX (Remote)",
        "description": "Build responsive SaaS interfaces and interactive dashboards using React, TypeScript, Tailwind CSS, Redux, and modern Vite build pipelines.",
        "required_skills": ["React", "TypeScript", "Tailwind", "JavaScript", "Redux", "HTML", "CSS", "Vite", "Git"],
        "experience_level": "Mid Level"
    },
    {
        "title": "Machine Learning & AI Engineer",
        "company": "NeuralInsight AI",
        "location": "Boston, MA",
        "description": "Develop and deploy deep learning models, natural language processing pipelines, and LLM integrations. Experience with Python, PyTorch, TensorFlow, Scikit-learn, Hugging Face, and FastAPI is required.",
        "required_skills": ["Python", "PyTorch", "TensorFlow", "Scikit-learn", "Machine Learning", "NLP", "FastAPI", "Docker"],
        "experience_level": "Senior"
    }
]

def seed_initial_data(db: Session):
    """
    Seeds initial taxonomy skills and sample jobs if database is empty.
    """
    # Seed skills
    if db.query(Skill).count() == 0:
        skills_to_add = []
        for category, skills in SKILL_TAXONOMY.items():
            for name in skills:
                skills_to_add.append(Skill(name=name, category=category))
        db.bulk_save_objects(skills_to_add)
        db.commit()

    # Seed sample jobs
    if db.query(Job).count() == 0:
        for job_data in SAMPLE_JOBS:
            job = Job(
                title=job_data["title"],
                company=job_data["company"],
                location=job_data["location"],
                description=job_data["description"],
                required_skills=job_data["required_skills"],
                experience_level=job_data["experience_level"]
            )
            db.add(job)
        db.commit()
