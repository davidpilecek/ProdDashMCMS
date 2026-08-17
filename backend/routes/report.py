from flask import Blueprint, jsonify, request, send_file
from io import BytesIO

from services.report_service import ReportService


report_bp = Blueprint(
    "report",
    __name__,
    url_prefix="/api",
)

report_service = ReportService()


@report_bp.post("/report")
def generate_report():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "success": False,
            "error": "Request body is required.",
        }), 400

    month = data.get("month")
    year = data.get("year")

    if not isinstance(month, int) or not 1 <= month <= 12:
        return jsonify({
            "success": False,
            "error": "Invalid month.",
        }), 400

    if not isinstance(year, int):
        return jsonify({
            "success": False,
            "error": "Invalid year.",
        }), 400

    try:

        pdf_bytes = report_service.generate_pdf(
            month=month,
            year=year,
        )

        return send_file(
            BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=(
                f"production_report_"
                f"{year}_{month:02d}.pdf"
            ),
        )

    except Exception as error:
        print(error)
        return jsonify({
            "success": False,
            "error": "Failed to generate report.",
        }), 500