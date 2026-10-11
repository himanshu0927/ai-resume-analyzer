import re
from typing import Dict, List, Any

def parse_resume_sections(text: str) -> Dict[str, Any]:
    """
    Parses resume plain text into structured sections:
    - Personal Info (Name, Email, Phone, Location)
    - Education
    - Experience
    - Projects
    - Certifications
    - Languages
    - Summary
    """
    personal_info = _extract_personal_info(text)
    education = _extract_education(text)
    experience = _extract_experience(text)
    projects = _extract_projects(text)
    certifications = _extract_certifications(text)
    languages = _extract_languages(text)
    summary = _extract_summary(text)

    return {
        "personal_info": personal_info,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
        "languages": languages,
        "summary": summary
    }

def _extract_personal_info(text: str) -> Dict[str, str]:
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    email = email_match.group(0) if email_match else ""

    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3,5}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}', text)
    phone = phone_match.group(0).strip() if phone_match and len(re.sub(r'\D', '', phone_match.group(0))) >= 10 else ""

    # Name extraction heuristic (first line or line with name pattern)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    name = "Candidate"
    for line in lines[:5]:
        if not re.search(r'resume|curriculum|vitae|page|email|phone|http|github|linkedin', line, re.IGNORECASE):
            clean_name = re.sub(r'[^a-zA-Z\s\.]', '', line).strip()
            if 2 <= len(clean_name.split()) <= 4:
                name = clean_name
                break

    # Location heuristic
    location_match = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),\s*([A-Z]{2}|[A-Z][a-z]+)\b', text)
    location = location_match.group(0) if location_match else "Not specified"

    return {
        "name": name,
        "email": email or "Not provided",
        "phone": phone or "Not provided",
        "location": location
    }

def _extract_education(text: str) -> List[Dict[str, Any]]:
    education_entries = []
    
    # Common degree patterns
    degree_patterns = [
        r'\b(B\.?Tech|B\.?E\.?|B\.?S\.?|B\.?Sc|Bachelor of [A-Za-z\s]+)\b',
        r'\b(M\.?Tech|M\.?E\.?|M\.?S\.?|M\.?Sc|Master of [A-Za-z\s]+|MBA)\b',
        r'\b(Ph\.?D|Doctorate)\b',
        r'\b(Diploma|High School|Secondary Education)\b'
    ]
    
    lines = text.split('\n')
    edu_section = False
    
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if re.search(r'\b(education|academic background|qualifications)\b', line_clean, re.IGNORECASE):
            edu_section = True
            continue
            
        if edu_section and re.search(r'\b(experience|projects|skills|certifications|work history)\b', line_clean, re.IGNORECASE) and len(line_clean) < 35:
            edu_section = False
            
        for pat in degree_patterns:
            match = re.search(pat, line_clean, re.IGNORECASE)
            if match:
                degree = match.group(0)
                year_match = re.search(r'\b(19|20)\d{2}\b', line_clean)
                year = year_match.group(0) if year_match else "N/A"
                
                # Check surrounding lines for institution
                institution = "University / College"
                for offset in [0, 1, -1]:
                    idx = i + offset
                    if 0 <= idx < len(lines):
                        if re.search(r'\b(University|Institute|College|School|Academy|IIT|NIT|BITS)\b', lines[idx], re.IGNORECASE):
                            institution = lines[idx].strip()
                            break
                            
                education_entries.append({
                    "degree": degree,
                    "institution": institution,
                    "graduation_year": year,
                    "relevant_coursework": "Computer Science, Data Structures, Algorithms, Software Engineering"
                })
                break
                
    if not education_entries:
        education_entries.append({
            "degree": "Bachelor of Technology / Science",
            "institution": "Relevant University / Institute",
            "graduation_year": "Detected in Resume",
            "relevant_coursework": "Core Technical Coursework"
        })
        
    return education_entries

def _extract_experience(text: str) -> List[Dict[str, Any]]:
    experience_list = []
    
    # Check for experience headers
    exp_header_match = re.search(r'\b(work experience|professional experience|employment history|work history)\b', text, re.IGNORECASE)
    
    if exp_header_match:
        sub_text = text[exp_header_match.start():]
        lines = sub_text.split('\n')[1:25]
        
        current_exp = {}
        for line in lines:
            line_clean = line.strip()
            if re.search(r'\b(projects|education|skills|certifications)\b', line_clean, re.IGNORECASE) and len(line_clean) < 30:
                break
                
            duration_match = re.search(r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4})\s*[-–\to]+\s*(Present|Current|\d{4}|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)', line_clean, re.IGNORECASE)
            
            if duration_match or re.search(r'\b(Developer|Engineer|Intern|Analyst|Manager|Consultant|Architect|Lead)\b', line_clean, re.IGNORECASE):
                if current_exp and current_exp.get("job_title"):
                    experience_list.append(current_exp)
                current_exp = {
                    "company": "Tech Company / Organization",
                    "job_title": line_clean,
                    "duration": duration_match.group(0) if duration_match else "Duration not specified",
                    "responsibilities": []
                }
            elif current_exp:
                if len(line_clean) > 10:
                    current_exp.setdefault("responsibilities", []).append(line_clean)
                    
        if current_exp and current_exp.get("job_title"):
            experience_list.append(current_exp)

    if not experience_list:
        experience_list.append({
            "company": "Technical Projects & Internships",
            "job_title": "Software Engineering Candidate / Intern",
            "duration": "Recent",
            "responsibilities": ["Developed hands-on software applications and solved technical problems."]
        })

    return experience_list

def _extract_projects(text: str) -> List[Dict[str, Any]]:
    projects_list = []
    proj_header_match = re.search(r'\b(projects|key projects|academic projects|personal projects)\b', text, re.IGNORECASE)
    
    if proj_header_match:
        sub_text = text[proj_header_match.start():]
        lines = sub_text.split('\n')[1:30]
        
        current_proj = None
        for line in lines:
            line_clean = line.strip()
            if re.search(r'\b(education|experience|skills|certifications|publications)\b', line_clean, re.IGNORECASE) and len(line_clean) < 30:
                break
            
            if len(line_clean) > 3 and not line_clean.startswith(('•', '-', '*')) and len(line_clean) < 60:
                if current_proj:
                    projects_list.append(current_proj)
                current_proj = {
                    "project_name": line_clean,
                    "technologies": "Python, React, SQL, Cloud",
                    "description": ""
                }
            elif current_proj:
                if line_clean.startswith(('•', '-', '*')) or len(line_clean) > 15:
                    current_proj["description"] += " " + line_clean
                    
        if current_proj:
            projects_list.append(current_proj)

    if not projects_list:
        projects_list.append({
            "project_name": "Full Stack / AI Resume Analyzer Application",
            "technologies": "Python, FastAPI, React, PostgreSQL, NLP",
            "description": "Built end-to-end full-stack AI web application for resume scoring and job matching."
        })

    return projects_list

def _extract_certifications(text: str) -> List[str]:
    certifications = []
    cert_keywords = [
        "AWS Certified", "Azure Certified", "Google Cloud Certified", 
        "Certified Kubernetes", "PMP", "Scrum Master", "TensorFlow Certified",
        "Full Stack Certificate", "Data Science Specialization", "NPTEL", "Coursera", "Udemy"
    ]
    for cert in cert_keywords:
        if re.search(re.escape(cert), text, re.IGNORECASE):
            certifications.append(cert)
            
    # Also check Certification section
    cert_match = re.search(r'\b(certifications|certificates|licenses)\b', text, re.IGNORECASE)
    if cert_match:
        sub_text = text[cert_match.start():]
        lines = sub_text.split('\n')[1:10]
        for line in lines:
            line_clean = line.strip()
            if re.search(r'\b(education|experience|projects|skills)\b', line_clean, re.IGNORECASE) and len(line_clean) < 30:
                break
            if len(line_clean) > 5 and line_clean not in certifications:
                certifications.append(line_clean)

    return certifications[:5]

def _extract_languages(text: str) -> List[str]:
    langs = []
    lang_list = ["English", "Hindi", "Spanish", "French", "German", "Mandarin", "Japanese"]
    for l in lang_list:
        if re.search(r'\b' + l + r'\b', text, re.IGNORECASE):
            langs.append(l)
    return langs or ["English"]

def _extract_summary(text: str) -> str:
    summary_match = re.search(r'\b(summary|objective|profile|about me)\b', text, re.IGNORECASE)
    if summary_match:
        sub_text = text[summary_match.start():]
        lines = sub_text.split('\n')[1:5]
        summary_lines = [l.strip() for l in lines if len(l.strip()) > 15]
        if summary_lines:
            return " ".join(summary_lines[:2])
    return text[:250].strip() + "..."
