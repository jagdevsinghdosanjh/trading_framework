import os #noqa
from pathlib import Path
from fpdf import FPDF
from typing import List


def generate_pdf_report(image_paths: List[str], output_path: str = "Trading_Report.pdf") -> None:
    """
    Combines multiple PNG charts into a single PDF report.
    Each image is placed on its own page with its title.

    Args:
        image_paths (List[str]): List of PNG file paths.
        output_path (str): Output PDF filename.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)

    for img_path in image_paths:
        title = Path(img_path).stem.replace("_", " ")

        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, title, ln=True, align="C")

        # Add image (centered)
        pdf.image(img_path, x=10, y=25, w=190)

    pdf.output(output_path)
    print(f"\n📄 PDF report saved as: {output_path}")
