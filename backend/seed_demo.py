import os
from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.services.auth_service import hash_password
from app.api.resumes import _perform_resume_analysis

DEMO_RESUME_TEXT = """
Alex Morgan
Email: alex.morgan@example.com
Phone: +1 (555) 234-5678
Location: Seattle, WA

PROFESSIONAL SUMMARY
Senior Full Stack & AI Engineer with 4+ years of experience designing scalable web microservices, REST APIs, and machine learning data pipelines.

SKILLS
Programming Languages: Python, JavaScript, TypeScript, SQL, HTML, CSS, C++
Web Frameworks: React, FastAPI, Node.js, Express, Django, Tailwind CSS, Redux
Databases: PostgreSQL, MongoDB, Redis, MySQL
Cloud & DevOps: Docker, Kubernetes, AWS, Git, GitHub Actions, Linux, CI/CD
AI & Data Science: TensorFlow, Scikit-learn, Pandas, NumPy, Machine Learning, Deep Learning, NLP

WORK EXPERIENCE
Full Stack Software Engineer | TechNova Solutions
Jan 2022 - Present
- Architected asynchronous microservices using Python, FastAPI, PostgreSQL, and Redis caching.
- Designed responsive SaaS frontend interfaces with React, TypeScript, and Tailwind CSS.
- Deployed containerized applications to AWS ECS using Docker and GitHub Actions CI/CD pipelines.

Software Developer Intern | DataSphere Systems
Jun 2020 - Dec 2021
- Developed ETL pipelines using Pandas and SQL to analyze customer engagement data.
- Built RESTful API endpoints for external client integrations.

EDUCATION
Bachelor of Technology (B.Tech) in Computer Science
Pacific Institute of Technology, 2021
Coursework: Data Structures, Algorithms, Database Systems, Software Engineering, Machine Learning

KEY PROJECTS
AI Resume Analyzer & Job Matcher
- Developed full-stack web application using FastAPI, React, PostgreSQL, and spaCy NLP engine.
- Implemented real-time PDF/DOCX parsing, skill taxonomy extraction, and job match scoring algorithms.

CERTIFICATIONS
- AWS Certified Developer Associate
- TensorFlow Developer Certificate
"""

def seed_demo_user_and_resume():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        demo_user = db.query(User).filter(User.email == "demo@example.com").first()
        if not demo_user:
            demo_user = User(
                name="Alex Morgan",
                email="demo@example.com",
                password_hash=hash_password("demo1234")
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
            print("Created Demo User: demo@example.com / demo1234")

        existing_resume = db.query(Resume).filter(Resume.user_id == demo_user.id).first()
        if not existing_resume:
            demo_path = os.path.join(os.path.dirname(__file__), "uploads", "sample_alex_morgan_resume.txt")
            os.makedirs(os.path.dirname(demo_path), exist_ok=True)
            with open(demo_path, "w", encoding="utf-8") as f:
                f.write(DEMO_RESUME_TEXT)

            resume = Resume(
                user_id=demo_user.id,
                filename="Alex_Morgan_FullStack_Resume.pdf",
                file_path=demo_path,
                file_type="PDF",
                extracted_text=DEMO_RESUME_TEXT
            )
            db.add(resume)
            db.commit()
            db.refresh(resume)

            _perform_resume_analysis(resume, demo_user.id, db)
            print("Seeded sample resume & ran initial analysis successfully!")
        else:
            print("Demo resume already exists.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_demo_user_and_resume()
