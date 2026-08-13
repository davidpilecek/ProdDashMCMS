from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


class ReportService:

    def __init__(self):
        self.template_dir = (
            Path(__file__).resolve().parent.parent
            / "reports"
            / "templates"
        )

    def generate_pdf(
        self,
        month: int,
        year: int,
    ) -> bytes:

        # TODO:
        # 1. Retrieve production data
        # 2. Prepare report data
        # 3. Render selected template

        output_path = (
            self.template_dir / "test_report.pdf"
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        pdf = canvas.Canvas(
            str(output_path),
            pagesize=A4,
        )

        width, height = A4

        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(
            50,
            height - 60,
            "Production Report",
        )

        pdf.setFont("Helvetica", 12)
        pdf.drawString(
            50,
            height - 90,
            f"Period: {month:02d}/{year}",
        )

        pdf.save()

        return output_path.read_bytes()