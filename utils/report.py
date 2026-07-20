"""
report.py
Builds a downloadable PDF health report summarizing a single prediction:
inputs, result, contributing factors, and growth tracker readout.
"""

from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)

from utils.prediction import FEATURE_LABELS

MINT = colors.HexColor("#2E6E68")
CORAL = colors.HexColor("#C4453B")
LIGHT_MINT = colors.HexColor("#E4F4F0")
LIGHT_CORAL = colors.HexColor("#FDEAE7")
MUTED = colors.HexColor("#5a6a75")


def generate_report_pdf(raw_input: dict, result: dict, risk_factors: list = None, growth_info: list = None) -> bytes:
    risk_factors = risk_factors or []
    growth_info = growth_info or []
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=1.6 * cm, bottomMargin=1.6 * cm,
        leftMargin=1.8 * cm, rightMargin=1.8 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleCustom", parent=styles["Title"], textColor=MINT, fontSize=20, spaceAfter=2)
    subtitle_style = ParagraphStyle("Subtitle", parent=styles["Normal"], textColor=MUTED, fontSize=9, spaceAfter=14)
    h2_style = ParagraphStyle("H2Custom", parent=styles["Heading2"], textColor=MINT, fontSize=13, spaceBefore=14, spaceAfter=6)
    body_style = ParagraphStyle("BodyCustom", parent=styles["Normal"], fontSize=9.5, leading=14)
    small_style = ParagraphStyle("SmallCustom", parent=styles["Normal"], fontSize=8, textColor=MUTED, leading=11)

    story = []

    # ---------------- Header ----------------
    story.append(Paragraph("NeoCare — Newborn Health Report", title_style))
    story.append(Paragraph(
        f"Generated {datetime.now().strftime('%d %B %Y, %I:%M %p')}", subtitle_style
    ))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#D5E6E2"), thickness=1))

    # ---------------- Result banner ----------------
    is_healthy = result["is_healthy"]
    banner_bg = LIGHT_MINT if is_healthy else LIGHT_CORAL
    banner_fg = MINT if is_healthy else CORAL
    banner_text = (
        f"Result: {'HEALTHY' if is_healthy else 'AT RISK'}  "
        f"({result['healthy_prob']*100:.1f}% healthy / {result['at_risk_prob']*100:.1f}% at-risk confidence)"
    )
    banner_style = ParagraphStyle("Banner", parent=styles["Normal"], fontSize=13, textColor=banner_fg, alignment=1, spaceBefore=10, spaceAfter=10)
    banner_table = Table([[Paragraph(banner_text, banner_style)]], colWidths=[17 * cm])
    banner_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), banner_bg),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0, banner_bg),
    ]))
    story.append(banner_table)

    # ---------------- Contributing factors ----------------
    if not is_healthy and risk_factors:
        story.append(Paragraph("Contributing Factors", h2_style))
        for f in risk_factors:
            if f["direction"] == "high":
                line = f"&#8226; <b>{f['label']}</b> is elevated at <b>{f['value']}</b> (healthy typical: ~{f['healthy_typical']})"
            elif f["direction"] == "low":
                line = f"&#8226; <b>{f['label']}</b> is lower than typical at <b>{f['value']}</b> (healthy typical: ~{f['healthy_typical']})"
            else:
                line = f"&#8226; <b>{f['label']}</b> is <b>{f['value']}</b>, differing from the typical healthy pattern ({f['healthy_typical']})"
            story.append(Paragraph(line, body_style))
        story.append(Paragraph(
            "This is a data-driven heuristic (how unusual each value is, weighted by how much "
            "the model relies on it) — not a clinical diagnosis.", small_style
        ))

    # ---------------- Growth tracker (optional section) ----------------
    if growth_info:
        story.append(Paragraph("Growth Tracker", h2_style))
        growth_rows = [["Measurement", "Value", "Typical Range (this dataset)", "Status"]]
        for g in growth_info:
            status_label = {"normal": "Normal", "low": "Below typical", "high": "Above typical"}[g["status"]]
            growth_rows.append([
                g["label"],
                f"{g['value']} {g['unit']}",
                f"{g['p10']:.1f} - {g['p90']:.1f} {g['unit']}",
                status_label,
            ])
        growth_table = Table(growth_rows, colWidths=[5.5 * cm, 3 * cm, 5.5 * cm, 3 * cm])
        growth_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), MINT),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 8.5),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F6FBFA")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5E6E2")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(growth_table)

    # ---------------- Full input values ----------------
    story.append(Paragraph("All Values Submitted", h2_style))
    input_rows = [["Field", "Value"]]
    for key, value in raw_input.items():
        input_rows.append([FEATURE_LABELS.get(key, key), str(value)])
    input_table = Table(input_rows, colWidths=[8.5 * cm, 8.5 * cm])
    input_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#77B7E8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F8FC")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5E6E2")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(input_table)

    # ---------------- Disclaimer ----------------
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#D5E6E2"), thickness=1))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "This report is generated by NeoCare, an educational demo application, and is "
        "<b>not a certified medical device or diagnosis</b>. Always consult a qualified "
        "pediatrician or neonatal specialist for real clinical decisions.", small_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()