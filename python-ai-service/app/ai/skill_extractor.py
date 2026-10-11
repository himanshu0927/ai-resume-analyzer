import re
from typing import Dict, List, Any
from app.ai.skill_taxonomy import SKILL_TAXONOMY, SKILL_ALIASES

def extract_skills(text: str) -> Dict[str, Any]:
    text_lower = text.lower()
    detected_skills_set = set()
    skill_categories_map: Dict[str, str] = {}
    
    canonical_to_category: Dict[str, str] = {}
    for cat, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            canonical_to_category[skill] = cat

    for category, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            if _match_skill_in_text(skill, text_lower):
                detected_skills_set.add(skill)
                skill_categories_map[skill] = category

    for alias, canonical in SKILL_ALIASES.items():
        if _match_skill_in_text(alias, text_lower):
            detected_skills_set.add(canonical)
            category = canonical_to_category.get(canonical, "Tools & Platforms")
            skill_categories_map[canonical] = category

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
    skill_lower = skill_str.lower()
    if skill_lower == "c++": return bool(re.search(r'\bc\+\+\b|c\+\+', text_lower))
    elif skill_lower == "c#": return bool(re.search(r'\bc\#\b|c\#', text_lower))
    elif skill_lower == "c": return bool(re.search(r'\b(c programming|language c|c language|c/c\+\+)\b', text_lower))
    elif skill_lower == "r": return bool(re.search(r'\b(r language|r programming)\b', text_lower))
    
    pattern = r'(?<![a-zA-Z0-9_\-\.])' + re.escape(skill_lower) + r'(?![a-zA-Z0-9_\-\.])'
    return bool(re.search(pattern, text_lower))
