# System Architecture Specification

## AI Resume Analyzer & Job Matcher

### System Dataflow
1. **Upload & Ingestion:**
   User uploads a PDF or DOCX file. Backend validates extension and file size (<10MB). `pdfplumber`/`pypdf` or `python-docx` parses raw text.
2. **Entity & Skill Extraction:**
   `skill_extractor.py` scans text against 100+ skill taxonomy items and aliases, avoiding false positives via regex word boundaries.
3. **Scoring Pipeline:**
   `score_calculator.py` computes weighted component scores:
   - Skills Depth (25%)
   - Work Experience (20%)
   - Technical Projects (20%)
   - Education (15%)
   - Certifications (5%)
   - Profile Completeness (5%)
   - Keyword Relevance (5%)
   - Formatting / Length (5%)
4. **LLM / Local Fallback:**
   If `LLM_API_KEY` is present, queries OpenAI API for feedback. If absent or offline, local deterministic NLP handles feedback without crashing.
5. **Job Matcher:**
   Calculates token intersection and skill overlap % against candidate resume.
6. **Report Generation:**
   `pdf_service.py` builds PDF document bytes using ReportLab and streams directly to client.
