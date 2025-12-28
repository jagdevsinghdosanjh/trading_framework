from fpdf import FPDF
from pathlib import Path
from PIL import Image
import datetime


def generate_pdf_report(image_paths, metrics, output="Report.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False)

    # COVER PAGE
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 20, "Trading Strategy Report", ln=True, align="C")

    pdf.set_font("Arial", "", 14)
    pdf.ln(10)
    for k, v in metrics.items():
        pdf.cell(0, 10, f"{k}: {v}", ln=True)

    # CHART PAGES
    for img_path in image_paths:
        img = Image.open(img_path).convert("RGB")
        temp = Path(img_path).with_suffix(".jpg")
        img.save(temp)

        pdf.add_page()
        pdf.image(str(temp), x=10, y=10, w=190)

        temp.unlink()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    pdf.output(f"Report_{timestamp}.pdf")
