import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_resume_pdf_report(analysis_data: dict, resume_filename: str) -> bytes:
    """
    Generates a professional PDF analysis report using ReportLab.
    Returns PDF bytes.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1E3A8A'),
        fontName='Helvetica-Bold',
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#475569'),
        spaceAfter=15
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1E40AF'),
        fontName='Helvetica-Bold',
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # Title Banner
    story.append(Paragraph("AI Resume Analysis Report", title_style))
    story.append(Paragraph(f"Document File: <b>{resume_filename}</b> | Date: Generated via AI Resume Engine", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceAfter=15))

    # Overall Score Box
    score = analysis_data.get("overall_score", 0.0)
    score_color = "#10B981" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"
    
    score_html = f"""
    <font size="16"><b>Overall Resume Score: <font color="{score_color}">{score} / 100</font></b></font><br/>
    <font size="9" color="#64748B">Note: This is an analytical Resume Score based on structure, skills depth, and content completeness.</font>
    """
    story.append(Paragraph(score_html, body_style))
    story.append(Spacer(1, 10))

    # Personal Information Section
    p_info = analysis_data.get("personal_info", {})
    story.append(Paragraph("Candidate Profile Summary", section_heading))
    profile_data = [
        [Paragraph("<b>Name:</b>", body_style), Paragraph(str(p_info.get("name", "N/A")), body_style)],
        [Paragraph("<b>Email:</b>", body_style), Paragraph(str(p_info.get("email", "N/A")), body_style)],
        [Paragraph("<b>Phone:</b>", body_style), Paragraph(str(p_info.get("phone", "N/A")), body_style)],
        [Paragraph("<b>Location:</b>", body_style), Paragraph(str(p_info.get("location", "N/A")), body_style)]
    ]
    t_profile = Table(profile_data, colWidths=[100, 430])
    t_profile.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(t_profile)
    story.append(Spacer(1, 10))

    # Component Scores Table
    story.append(Paragraph("Score Factor Breakdown", section_heading))
    factors = analysis_data.get("score_factors", [])
    table_data = [[Paragraph("<b>Factor</b>", body_style), Paragraph("<b>Weight</b>", body_style), Paragraph("<b>Score</b>", body_style), Paragraph("<b>Status</b>", body_style)]]
    
    for f in factors:
        table_data.append([
            Paragraph(str(f.get("factor")), body_style),
            Paragraph(str(f.get("weight")), body_style),
            Paragraph(f"{f.get('score')} / 100", body_style),
            Paragraph(str(f.get("status")), body_style)
        ])
        
    t_factors = Table(table_data, colWidths=[200, 100, 100, 130])
    t_factors.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EFF6FF')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#1E40AF')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t_factors)
    story.append(Spacer(1, 10))

    # Extracted Skills Section
    story.append(Paragraph("Detected Technical & Soft Skills", section_heading))
    raw_data = analysis_data.get("raw_extracted_data", {})
    categorized_skills = raw_data.get("categorized_skills", {})
    
    skill_rows = []
    for cat, s_list in categorized_skills.items():
        if s_list:
            skills_str = ", ".join(s_list)
            skill_rows.append([Paragraph(f"<b>{cat}:</b>", body_style), Paragraph(skills_str, body_style)])
            
    if skill_rows:
        t_skills = Table(skill_rows, colWidths=[150, 380])
        t_skills.setStyle(TableStyle([
            ('PADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#F1F5F9')),
        ]))
        story.append(t_skills)
    else:
        story.append(Paragraph("No structured technical skills detected.", body_style))
    story.append(Spacer(1, 10))

    # Prioritized Improvement Suggestions
    story.append(Paragraph("Actionable Improvement Suggestions", section_heading))
    suggestions = analysis_data.get("suggestions", [])
    for sug in suggestions:
        priority = sug.get("priority", "Medium")
        p_color = "#DC2626" if priority == "High" else "#D97706" if priority == "Medium" else "#2563EB"
        sug_text = f"<b><font color='{p_color}'>[{priority} Priority]</font></b> {sug.get('text')}"
        story.append(Paragraph(sug_text, body_style))
        story.append(Spacer(1, 4))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
