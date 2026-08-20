import re
from xml.sax.saxutils import escape

from reportlab.lib import colors# type: ignore
from reportlab.lib.enums import TA_CENTER# type: ignore
from reportlab.lib.pagesizes import A4# type: ignore
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle# type: ignore
from reportlab.lib.units import mm # type: ignore
from reportlab.platypus import HRFlowable # type: ignore
from reportlab.platypus import (# type: ignore
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    Image,
    Preformatted,
    XPreformatted,
    KeepTogether
)

CODE_TOKEN_PATTERN = re.compile(
    r"//[^\n]*|/\*[\s\S]*?\*/|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|"
    r"#[^\n]*|\b(?:alignas|auto|bool|break|case|catch|class|const|continue|default|do|else|"
    r"for|if|namespace|new|private|public|return|sizeof|static|struct|switch|template|this|"
    r"throw|try|using|virtual|void|while)\b|\b(?:char|double|float|int|long|size_t|string|unsigned|vector)\b|"
    r"\b\d+(?:\.\d+)?\b"
)


def highlighted_code(code):
    highlighted = []
    last_end = 0

    for match in CODE_TOKEN_PATTERN.finditer(code):
        highlighted.append(escape(code[last_end:match.start()]))
        token = escape(match.group())

        if match.group().startswith(("//", "/*")):
            token_color = "#6b7280"
        elif match.group().startswith(("\"", "'")):
            token_color = "#15803d"
        elif match.group().startswith("#"):
            token_color = "#9333ea"
        elif match.group()[0].isdigit():
            token_color = "#c2410c"
        elif match.group() in {
            "char", "double", "float", "int", "long", "size_t", "string", "unsigned", "vector"
        }:
            token_color = "#0369a1"
        else:
            token_color = "#b91c1c"

        highlighted.append(f'<font color="{token_color}">{token}</font>')
        last_end = match.end()

    highlighted.append(escape(code[last_end:]))
    return "".join(highlighted)


def paragraph_text(text):
    return escape(str(text)).replace("\\n", "<br/>")


def generate_pdf(
    assignment_num,
    assignment_name,
    assignment_statement,
    theory,
    time_complexity,
    space_complexity,
    complexity_analysis,
    code,
    outputs,
    averages,
    graph_path
):
    pdf_name = f"Assignment_{assignment_num}.pdf"
    doc = SimpleDocTemplate(pdf_name, pagesize = A4, 
                            rightMargin = 20 * mm, leftMargin = 20*mm, topMargin = 20*mm, bottomMargin = 20*mm)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCustom",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=22,
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "HeadingCustom",
        parent=styles["Heading1"],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["BodyText"],
        fontSize=12.5,
        leading=16
    )

    code_style = ParagraphStyle(
        "CodeCustom",
        fontName="Courier",
        fontSize=9.5,
        leading=9
    )

    output_style = ParagraphStyle(
        "CodeCustom",
        fontName="Courier-Bold",
        fontSize=8.5,
        leading=9,
        textColor=colors.white
    )

    story = []

    story.append(
        Paragraph(
            f"DAA PRACTICAL ASSIGNMENT",
            title_style
        )
    )

    story.append(
        Paragraph(
            f"Assignment {assignment_num}: {assignment_name}",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 15))

    info = {}
    with open("info.txt", "r", encoding="utf-8") as info_file:
        for line in info_file:
            key, separator, value = line.partition(":")
            if separator:
                info[key.strip()] = value.strip()

    for key, value in info.items():
        story.append(
            Paragraph(
                f"<b>{key}:</b> {value}",
                normal_style
            )
        )

    story.append(Spacer(1, 12))

    story.append(
        Paragraph("1. ASSIGNMENT STATEMENT", heading_style)
    )
    story.append(
        Paragraph(
            assignment_statement,
            normal_style
        )
    )

    story.append(
        Paragraph("2. THEORY", heading_style)
    )
    story.append(Paragraph(paragraph_text(theory), normal_style))

    story.append(
        Paragraph("3. CODE", heading_style)
    )

    story.append(
        Table(
            [
                [XPreformatted(highlighted_code(line), code_style)]
                for line in code.splitlines() or [""]
            ],
            colWidths=[170 * mm],
            style=TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#bababa")),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f4f4f4")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ])
        )
    )

    story.append(PageBreak())

    story.append(
        Paragraph("4. OUTPUT", heading_style)
    )

    for output in outputs:
        output_block = Table(
            [[Preformatted("\n\n".join(output), output_style)]],
            colWidths=[170 * mm]
        )

        output_block.setStyle(
            TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#555555")),
                ("BACKGROUND", (0, 0), (-1, -1), colors.black),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ])
        )

        story.append(output_block)

        story.append(Spacer(1, 10))

    story.append(PageBreak())
    story.append(
        Paragraph("5. COMPLEXITY ANALYSIS", heading_style)
    )
    story.append(Paragraph(f"<b>Time Complexity:</b> {paragraph_text(time_complexity)}", normal_style))
    story.append(Paragraph(f"<b>Space Complexity:</b> {paragraph_text(space_complexity)}", normal_style))
    story.append(Paragraph(f"<b>Conclusion:</b> {paragraph_text(complexity_analysis)}", normal_style))

    categories = list(
        averages[list(averages.keys())[0]].keys()
    )

    table_data = [
        ["Data Size"] + categories
    ]

    for size in averages:

        row = [str(size)]

        for category in categories:
            row.append(
                f"{averages[size][category]:.2f}"
            )

        table_data.append(row)

    table = Table(
        table_data,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#222222")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#eeeeee")])
        ])
    )

    graph = Image(graph_path)

    graph.drawHeight = 110 * mm
    graph.drawWidth = 170 * mm

    story.append(
        KeepTogether([
            Paragraph("6. PERFORMANCE RESULTS", heading_style),
            table,
            Paragraph("7. GRAPHICAL ANALYSIS", heading_style),
            graph
        ])
    )

    story.append(Spacer(1, 10))
    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#555555"),
            spaceBefore=4,
            spaceAfter=10
        )
    )

    doc.build(story)

    print(f"\nPDF generated: {pdf_name}")