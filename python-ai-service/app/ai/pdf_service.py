import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_report(analysis_data: dict, filename: str) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor('#1E3A8A'))
    heading_style = ParagraphStyle('DocHeading', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor('#1E40AF'))
    body_style = ParagraphStyle('DocBody', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor('#1E293B'))

    story = [
        Paragraph("AI Resume Analysis Report", title_style),
        Paragraph(f"Document File: <b>{filename}</b>", body_style),
        HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceAfter=15),
        Paragraph(f"<b>Overall Resume Score: <font color='#10B981'>{analysis_data.get('overall_score', 0.0)} / 100</font></b>", body_style),
        Spacer(1, 10),
        Paragraph("Candidate Profile Summary", heading_style),
    ]

    p_info = analysis_data.get("personal_info", {})
    profile_table = [
        [Paragraph("<b>Name:</b>", body_style), Paragraph(str(p_info.get("name", "N/A")), body_style)],
        [Paragraph("<b>Email:</b>", body_style), Paragraph(str(p_info.get("email", "N/A")), body_style)],
        [Paragraph("<b>Phone:</b>", body_style), Paragraph(str(p_info.get("phone", "N/A")), body_style)],
        [Paragraph("<b>Location:</b>", body_style), Paragraph(str(p_info.get("location", "N/A")), body_style)]
    ]
    t = Table(profile_table, colWidths=[100, 430])
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0'))]))
    story.append(t)
    story.append(Spacer(1, 15))

    story.append(Paragraph("Score Factor Breakdown", heading_style))
    factors = analysis_data.get("score_factors", [])
    f_data = [[Paragraph("<b>Factor</b>", body_style), Paragraph("<b>Weight</b>", body_style), Paragraph("<b>Score</b>", body_style), Paragraph("<b>Status</b>", body_style)]]
    for f in factors:
        f_data.append([Paragraph(str(f.get("factor")), body_style), Paragraph(str(f.get("weight")), body_style), Paragraph(f"{f.get('score')} / 100", body_style), Paragraph(str(f.get("status")), body_style)])
    
    t_f = Table(f_data, colWidths=[200, 100, 100, 130])
    t_f.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EFF6FF')), ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1'))]))
    story.append(t_f)

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
