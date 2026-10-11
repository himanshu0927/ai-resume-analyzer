import re
from typing import Dict, List, Any
from app.ai.skill_taxonomy import SKILL_TAXONOMY, SKILL_ALIASES

def extract_skills(text: str) -> Dict[str, Any]:
    """
    Extracts skills from text based on taxonomy and aliases.
    Returns:
    {
        "all_skills": ["Python", "SQL", "React", ...],
        "categorized_skills": {
            "Programming Languages": ["Python", "JavaScript"],
            "Databases": ["PostgreSQL", "MongoDB"],
            ...
        },
        "skill_details": [
            {"name": "Python", "category": "Programming Languages", "confidence": 0.95},
            ...
        ]
    }
    """
    text_lower = text.lower()
    detected_skills_set = set()
    skill_categories_map: Dict[str, str] = {}
    
    # Map all canonical taxonomy skills to their categories
    canonical_to_category: Dict[str, str] = {}
    for cat, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            canonical_to_category[skill] = cat

    # Search for canonical taxonomy skills
    for category, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            if _match_skill_in_text(skill, text_lower):
                detected_skills_set.add(skill)
                skill_categories_map[skill] = category

    # Search for alias matches
    for alias, canonical in SKILL_ALIASES.items():
        if _match_skill_in_text(alias, text_lower):
            detected_skills_set.add(canonical)
            category = canonical_to_category.get(canonical, "Tools & Platforms")
            skill_categories_map[canonical] = category

    # Build response structures
    categorized: Dict[str, List[str]] = {cat: [] for cat in SKILL_TAXONOMY.keys()}
    skill_details = []
    
    for skill in sorted(list(detected_skills_set)):
        cat = skill_categories_map.get(skill, "Tools & Platforms")
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append(skill)
        skill_details.append({
            "name": skill,
            "category": cat,
            "confidence": 0.95 if cat != "Soft Skills" else 0.85
        })

    return {
        "all_skills": sorted(list(detected_skills_set)),
        "categorized_skills": categorized,
        "skill_details": skill_details,
        "total_count": len(detected_skills_set)
    }

def _match_skill_in_text(skill_str: str, text_lower: str) -> bool:
    """
    Matches skill with word boundary checks to avoid false positives
    (e.g., matching 'c' inside 'can' or 'java' inside 'javascript').
    """
    skill_lower = skill_str.lower()
    
    # Handle special character skills like C++, C#, .NET, CI/CD
    if skill_lower == "c++":
        return bool(re.search(r'\bc\+\+\b|c\+\+', text_lower))
    elif skill_lower == "c#":
        return bool(re.search(r'\bc\#\b|c\#', text_lower))
    elif skill_lower == "c":
        return bool(re.search(r'\b(c programming|language c|c language|c/c\+\+)\b', text_lower))
    elif skill_lower == "r":
        return bool(re.search(r'\b(r language|r programming|language r)\b', text_lower))
    elif skill_lower == "ai/ml":
        return bool(re.search(r'\bai/ml\b|\bai / ml\b', text_lower))
    elif skill_lower == "ci/cd":
        return bool(re.search(r'\bci/cd\b|\bci / cd\b', text_lower))
    
    # General word boundary check
    pattern = r'(?<![a-zA-Z0-9_\-\.])' + re.escape(skill_lower) + r'(?![a-zA-Z0-9_\-\.])'
    return bool(re.search(pattern, text_lower))
