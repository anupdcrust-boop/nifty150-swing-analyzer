"""Minimal, dependency-light Markdown -> PDF renderer (headers, paragraphs,
bold/code inline spans, pipe tables, horizontal rules) using reportlab.
Good enough for this project's docs; not a general Markdown engine."""
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak,
)

INLINE_PATTERNS = [
    (re.compile(r"\*\*(.+?)\*\*"), r"<b>\1</b>"),
    (re.compile(r"`([^`]+)`"), r'<font face="Courier" size="8.5">\1</font>'),
]


def inline(text: str) -> str:
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    for pat, repl in [
        (re.compile(r"\*\*(.+?)\*\*"), r"<b>\1</b>"),
        (re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)"), r"<i>\1</i>"),
        (re.compile(r"`([^`]+)`"), r'<font face="Courier" size="8.5">\1</font>'),
    ]:
        text = pat.sub(repl, text)
    return text


def parse_table(lines: list[str]) -> list[list[str]]:
    rows = []
    for line in lines:
        if re.match(r"^\s*\|?\s*-{2,}", line.replace("|", "")):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows


def build_story(md_text: str, styles) -> list:
    story = []
    lines = md_text.split("\n")
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("|"):
            table_lines = []
            while i < n and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            rows = parse_table(table_lines)
            if rows:
                cell_style = ParagraphStyle("cell", parent=styles["Normal"], fontSize=8, leading=10)
                header_style = ParagraphStyle("cellhdr", parent=cell_style, fontName="Helvetica-Bold")
                data = []
                for r_idx, row in enumerate(rows):
                    style = header_style if r_idx == 0 else cell_style
                    data.append([Paragraph(inline(c), style) for c in row])
                ncols = max(len(r) for r in data)
                data = [r + [Paragraph("", cell_style)] * (ncols - len(r)) for r in data]
                col_width = (LETTER[0] - 1.4 * inch) / ncols
                t = Table(data, colWidths=[col_width] * ncols, repeatRows=1)
                t.setStyle(TableStyle([
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2b2f38")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f3f5")]),
                ]))
                story.append(t)
                story.append(Spacer(1, 12))
            continue

        if stripped.startswith("### "):
            story.append(Paragraph(inline(stripped[4:]), styles["Heading3"]))
            i += 1
            continue
        if stripped.startswith("## "):
            story.append(Spacer(1, 6))
            story.append(Paragraph(inline(stripped[3:]), styles["Heading2"]))
            i += 1
            continue
        if stripped.startswith("# "):
            story.append(Paragraph(inline(stripped[2:]), styles["Title"]))
            i += 1
            continue

        if stripped.startswith("---"):
            story.append(Spacer(1, 6))
            story.append(HRFlowable(width="100%", color=colors.HexColor("#cccccc")))
            story.append(Spacer(1, 6))
            i += 1
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            bullet_lines = []
            while i < n and (lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ")):
                bullet_lines.append(lines[i].strip()[2:])
                i += 1
            for b in bullet_lines:
                story.append(Paragraph("&bull;&nbsp;&nbsp;" + inline(b), styles["Normal"]))
            story.append(Spacer(1, 6))
            continue

        # paragraph: accumulate until blank line
        para_lines = [stripped]
        i += 1
        while i < n and lines[i].strip() and not lines[i].strip().startswith(("#", "|", "-", "*")):
            para_lines.append(lines[i].strip())
            i += 1
        story.append(Paragraph(inline(" ".join(para_lines)), styles["Normal"]))
        story.append(Spacer(1, 8))

    return story


def main(src: str, dst: str):
    md_text = Path(src).read_text()
    styles = getSampleStyleSheet()
    styles["Normal"].fontSize = 9.5
    styles["Normal"].leading = 13
    styles["Heading2"].spaceBefore = 14
    styles["Heading3"].spaceBefore = 10

    doc = SimpleDocTemplate(
        dst, pagesize=LETTER,
        topMargin=0.7 * inch, bottomMargin=0.7 * inch,
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        title="STOCK RESEARCH Unified Framework v2.2 Addendum",
    )
    story = build_story(md_text, styles)
    doc.build(story)
    print(f"wrote {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
