# B.Tech Final Year Project Documentation
## AI Resume Analyzer & Job Matcher

**Degree Program:** Bachelor of Technology (B.Tech) in Computer Science & Engineering  
**Project Title:** AI-Powered Resume Analyzer & Job Matcher System  
**Version:** 1.0.0 (Production Release)  

---

### 1. Abstract
In today's dynamic technology job market, software engineers and candidates face significant hurdles tailoring their resumes for automated Applicant Tracking Systems (ATS) and specific job descriptions. This project presents **AI Resume Analyzer & Job Matcher**, an end-to-end full-stack web application designed to parse candidate resumes (PDF/DOCX), extract structured technical entity data, calculate transparent multi-factor analytical scores (0–100), and perform similarity matching against target job descriptions. 

The system leverages local Natural Language Processing (spaCy/regex taxonomy) and deterministic scoring algorithms with optional LLM API fallback support, ensuring operational independence even when external cloud APIs are absent.

---

### 2. Problem Statement
Traditional hiring systems rely on black-box ATS algorithms that reject resumes without actionable feedback. Candidates lack transparent visibility into:
1. Missing technical skills and keyword gaps relative to target job postings.
2. Section-level structural quality (formatting, project bullet metrics, and action verbs).
3. Non-biased target role suitability recommendations based strictly on skill taxonomies.

---

### 3. Key Objectives
- **Text Extraction:** Process unstructured PDF and DOCX documents cleanly without data loss.
- **Skill Extraction:** Categorize technical skills into 9 standardized domains (Programming, Web Dev, Databases, Cloud, DevOps, AI/ML, Data Science, Tools, Soft Skills).
- **Transparent Scoring Engine:** Compute separate scores for skills depth, work experience, projects, education, certifications, and formatting.
- **Job Description Matcher:** Calculate cosine/keyword similarity, matching skills, missing skills, and context bullet points for any pasted job posting.
- **Skill Gap & Roadmap:** Compare candidate profiles against target roles (e.g. Full Stack Developer, Data Scientist) and generate actionable project ideas and learning topics.
- **Exportable PDF Reports:** Stream professional PDF summary reports generated on-the-fly via ReportLab.

---

### 4. System Architecture
```
[ User Browser (React + TypeScript + Tailwind CSS) ]
                        │
                        ▼ (REST APIs / JSON)
        [ FastAPI Backend Service ]
          ├── Auth & JWT Security (bcrypt)
          ├── NLP Skill & Parser Engine
          ├── Multi-Factor Scoring Engine
          ├── Job Description Matcher
          ├── ReportLab PDF Generator
          └── Database Access (SQLAlchemy)
                        │
                        ▼
         [ PostgreSQL / SQLite Database ]
```

---

### 5. Database Schema & ER Design
The database consists of 8 relational entities:
- `users`: User identity, password hash (bcrypt), registration timestamps.
- `resumes`: Metadata for uploaded PDF/DOCX files, user foreign key, extracted raw text.
- `resume_analysis`: Overall score, component factor breakdown, extracted sections (JSON).
- `skills`: Extensible taxonomy repository of standard tech skills.
- `resume_skills`: Junction table storing extracted skills per resume with confidence ratings.
- `jobs`: Sample job descriptions and required skills.
- `job_matches`: Saved candidate job matching results.
- `recommendations`: Target role recommendations with explicit technical reasons.

---

### 6. Non-Discrimination & Ethics Compliance
The application enforces strict non-discrimination guidelines:
- Role recommendations and job matching scores are derived **exclusively** from technical skills, programming languages, framework experience, and academic background.
- Demographic traits (age, gender, ethnicity, location bias) are strictly excluded from recommendation and scoring pipelines.
- Scores are explicitly labeled as **“Resume Analysis Score”** for self-improvement and do not claim to predict hiring decisions or guarantee employment.

---

### 7. Future Scope
- Support for multi-lingual resume parsing (German, French, Spanish).
- OCR support for legacy scanned image resumes.
- Automated interview question generation based on detected skill gaps.
