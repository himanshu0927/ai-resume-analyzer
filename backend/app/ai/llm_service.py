import json
import logging
import requests
from typing import Dict, Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)

def generate_ai_resume_feedback(resume_text: str, current_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    If LLM_API_KEY is configured, calls LLM API to get enhanced qualitative feedback.
    Otherwise, gracefully returns rule-based feedback fallback without error.
    """
    api_key = settings.LLM_API_KEY
    if not api_key:
        logger.info("LLM_API_KEY is not set. Using local deterministic NLP fallback.")
        return _get_fallback_feedback(current_analysis)

    try:
        # Generic OpenAI/compatible REST API call
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        prompt = (
            f"Analyze the following candidate resume text and provide 3 high-impact improvement suggestions.\n"
            f"Resume Text Sample:\n{resume_text[:2000]}\n"
            f"Respond only with a JSON array of objects having keys 'priority' ('High'|'Medium'|'Low'), 'category', and 'text'."
        )
        payload = {
            "model": settings.LLM_MODEL or "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=8)
        if response.status_code == 200:
            res_data = response.json()
            content = res_data["choices"][0]["message"]["content"]
            parsed_json = json.loads(content)
            return {"enhanced_by_llm": True, "suggestions": parsed_json}
    except Exception as e:
        logger.warning(f"LLM API call failed or timed out: {e}. Falling back to local NLP analysis.")

    return _get_fallback_feedback(current_analysis)

def _get_fallback_feedback(current_analysis: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "enhanced_by_llm": False,
        "note": "Analysis performed using local deterministic spaCy/NLP rule engine.",
        "suggestions": current_analysis.get("suggestions", [])
    }
