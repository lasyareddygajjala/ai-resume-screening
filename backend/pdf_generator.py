from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

def generate_pdf(result, output_file):

    doc = SimpleDocTemplate(output_file)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Resume Screening Report</b>", styles["Title"]))
    story.append(Spacer(1, 20))

    table_data = [
        ["Candidate", result["candidate_name"]],
        ["Resume", result["filename"]],
        ["Category", result["category"]],
        ["Rank", str(result["rank"])],
        ["ATS Score", f"{result['score']}%"],
        ["Similarity", result["similarity"]],
        ["Recommendation", result["suitability"]]
    ]

    table = Table(table_data, colWidths=[120, 320])

    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.grey),
        ("BACKGROUND", (0,0), (0,-1), colors.lightblue),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    ]))

    story.append(table)
    story.append(Spacer(1,20))

    story.append(Paragraph("<b>Matched Skills</b>", styles["Heading2"]))
    for skill in result["matched_skills"]:
        story.append(Paragraph(f"• {skill}", styles["Normal"]))

    story.append(Spacer(1,10))

    story.append(Paragraph("<b>Missing Skills</b>", styles["Heading2"]))
    for skill in result["missing_skills"]:
        story.append(Paragraph(f"• {skill}", styles["Normal"]))

    story.append(Spacer(1,10))

    story.append(Paragraph("<b>Suggestions</b>", styles["Heading2"]))
    for suggestion in result["suggestions"]:
        story.append(Paragraph(f"• {suggestion}", styles["Normal"]))

    doc.build(story)