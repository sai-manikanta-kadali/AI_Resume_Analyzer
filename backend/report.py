from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def build_report(data):
    output = BytesIO()
    doc = SimpleDocTemplate(output, pagesize=A4, rightMargin=42, leftMargin=42, topMargin=42, bottomMargin=42)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Accent', parent=styles['Heading1'], textColor=colors.HexColor('#4d43c7'), fontSize=22, spaceAfter=8))
    story = [Paragraph('RESUMATE AI', styles['Accent']), Paragraph('Resume Intelligence Report', styles['Title']), Spacer(1, 12)]
    story.append(Paragraph(f"Target role: {data.get('target_role', 'Not specified')} | Date: {data.get('analysis_date', '')[:10]}", styles['BodyText']))
    story.append(Spacer(1, 16))
    story.append(Paragraph(f"ATS-style compatibility: {data.get('final_score', 0)}/100", styles['Heading2']))
    breakdown = [['Metric', 'Score'], ['Skill match', f"{data.get('skill_match', 0)}%"], ['Keyword match', f"{data.get('keyword_match', 0)}%"], ['Semantic similarity', f"{data.get('semantic_similarity', 0)}%"], ['Completeness', f"{data.get('completeness', 0)}%"], ['Formatting', f"{data.get('formatting', 0)}%"]]
    table = Table(breakdown, colWidths=[260, 120])
    table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#24232b')), ('TEXTCOLOR', (0,0), (-1,0), colors.white), ('GRID', (0,0), (-1,-1), .25, colors.lightgrey), ('PADDING', (0,0), (-1,-1), 8)]))
    story += [Spacer(1, 10), table, Spacer(1, 18), Paragraph('Matched skills', styles['Heading2']), Paragraph(', '.join(data.get('matched_skills', [])) or 'None detected', styles['BodyText']), Paragraph('Skills not detected', styles['Heading2']), Paragraph(', '.join(item.get('name', '') for item in data.get('missing_skills', [])) or 'None detected', styles['BodyText']), Paragraph('Strengths', styles['Heading2'])]
    story += [Paragraph(f'• {item}', styles['BodyText']) for item in data.get('strengths', [])]
    story.append(Paragraph('Areas to improve', styles['Heading2']))
    story += [Paragraph(f'• {item}', styles['BodyText']) for item in data.get('improvements', [])]
    story.append(Paragraph('Role-ready learning plan', styles['Heading2']))
    story += [Paragraph(f"• {item.get('skill')}: {item.get('proof')}", styles['BodyText']) for item in data.get('learning_plan', [])]
    story.append(Paragraph('Honest resume changes', styles['Heading2']))
    story += [Paragraph(f'• {item}', styles['BodyText']) for item in data.get('resume_rewrite', [])]
    template = data.get('tailored_resume', {})
    if template:
        story.append(Paragraph('Role-specific resume template', styles['Heading2']))
        story.append(Paragraph(template.get('notice', ''), styles['BodyText']))
        story.append(Paragraph(template.get('headline', ''), styles['BodyText']))
        story.append(Paragraph(f"Skills to verify: {', '.join(template.get('skills', []))}", styles['BodyText']))
        story += [Paragraph(f'• {item}', styles['BodyText']) for item in template.get('project_bullets', [])]
    doc.build(story)
    return output.getvalue()
