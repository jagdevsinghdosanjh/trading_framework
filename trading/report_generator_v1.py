from pathlib import Path
from fpdf import FPDF
from PIL import Image
from typing import List


def generate_pdf_report(image_paths: List[str], output_path: str = "Trading_Report.pdf") -> None:
    """
    Combines multiple PNG charts into a single PDF report.
    Ensures images exist, converts them to RGB, and embeds them safely.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)

    for img_path in image_paths:
        img_path = Path(img_path)

        if not img_path.exists():
            print(f"⚠️ Skipping missing image: {img_path}")
            continue

        # Convert PNG to RGB (fixes transparency issues)
        img = Image.open(img_path).convert("RGB")
        temp_jpg = img_path.with_suffix(".jpg")
        img.save(temp_jpg)

        title = img_path.stem.replace("_", " ")

        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, title, ln=True, align="C")

        pdf.image(str(temp_jpg), x=10, y=25, w=190)

        temp_jpg.unlink()  # remove temporary JPG

    pdf.output(output_path)
    print(f"\n📄 PDF report saved as: {output_path}")
