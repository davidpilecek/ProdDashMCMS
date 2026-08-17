from io import BytesIO

from pathlib import Path

from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib import styles
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    Flowable,
    Image,
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from services.report_graph_service import (
    generate_production_graph,
)

from services.production_service import (
    load_production_month,
)

from services.statistics_service import (
    calculate_production_statistics,
    )

BASE_DIR = Path(__file__).resolve().parent.parent

LOGO_PATH = (
    BASE_DIR
    / "reports"
    / "assets"
    / "logo_metris_wave.png"
)

# Report colors
PRIMARY = HexColor("#003a70")
SECONDARY = HexColor("#707070")
LIGHT_BACKGROUND = HexColor("#F3F5F6")
BORDER = HexColor("#dddddd")
TEXT = HexColor("#000f1a")
LIGHTGREY = HexColor("#f0f0f0")
GREY = HexColor("#dddddd")


def convert_runtime_to_days_hours(runtime: float) -> float:
    # Calculate the number of full days in the given time duration.
    time = runtime

    day = time // (24 * 3600)
    # Update the time variable to hold the remaining seconds after subtracting full days.
    time = time % (24 * 3600)

    # Calculate the number of full hours in the remaining time.
    hour = time // 3600
    # Update the time variable to hold the remaining seconds after subtracting full hours.
    time %= 3600

    # Calculate the number of full minutes in the remaining time.
    minutes = time // 60
    # Update the time variable to hold the remaining seconds after subtracting full minutes.
    time %= 60

    # The 'time' variable now represents the remaining seconds, which is the number of seconds.
    seconds = time

    return day, hour, minutes, seconds


class ReportHeader(Flowable):

    def __init__(
        self,
        logo_path: str,
        title: str,
        generated_text: str,
        logo_width: float,
        logo_height: float,
    ):
        super().__init__()

        self.logo_path = logo_path
        self.title = title
        self.generated_text = generated_text

        self.logo_width = logo_width
        self.logo_height = logo_height

        self.width = 180 * mm
        self.height = 40 * mm

    def draw(self):

        canvas = self.canv

        # --------------------------------------------------
        # Top row: Logo + generation date
        # --------------------------------------------------

        canvas.drawImage(
            self.logo_path,
            0,
            self.height - self.logo_height,
            width=self.logo_width,
            height=self.logo_height,
            preserveAspectRatio=True,
            mask="auto",
        )

        canvas.setFont(
            "Helvetica",
            10,
        )

        canvas.drawRightString(
            self.width,
            self.height - 5 * mm,
            self.generated_text,
        )

        # --------------------------------------------------
        # Report title
        # --------------------------------------------------

        canvas.setFont(
            "Helvetica-Bold",
            18,
        )

        canvas.drawString(
            0,
            0 * mm,
            self.title,
        )

class ReportService:

    def generate_pdf(
        self,
        month: int,
        year: int,
    ) -> bytes:

        data = load_production_month(
            month,
            year,
        )

        production_units = data["productionUnits"]
        segments = data["segments"]


        graph_bytes = generate_production_graph(
            segments=segments,
            month=month,
            year=year,
        )
        
        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=8 * mm,
            bottomMargin=15 * mm,
        )

        styles = getSampleStyleSheet()

        elements = []

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        header = ReportHeader(
            logo_path=str(LOGO_PATH),
            title=f"Production Report for {month:02d}/{year}",
            generated_text=(
                f"Generated on "
                f"{datetime.now().strftime('%d.%m.%Y %H:%M')}"
            ),
            logo_width=45 * mm,
            logo_height=25 * mm,
        )

        elements.append(header)

        elements.append(
            Spacer(1, 8 * mm)
        )

#  Graph
   
   
        # elements.append(
        #     Spacer(1, 8 * mm)
        # )

        # elements.append(
        #     Paragraph(
        #         "Production Overview",
        #         styles["Heading2"],
        #     )
        # )

        elements.append(
            Image(
                BytesIO(graph_bytes),
                width=175 * mm,
                height=70 * mm,
            )
        )

        elements.append(
            Spacer(1, 8 * mm)
        )

       # --------------------------------------------------
        # Monthly summary
        # --------------------------------------------------

        elements.append(
            Paragraph(
                "Monthly Summary",
                styles["Heading2"],
            )
        )


        statistics = calculate_production_statistics(
            segments=segments,
            selected_segment_id=segments[-1]["segmentId"]
        )

        monthly_rate = statistics["month"]["rate"]

        total_produced = 0

        for production_unit in production_units:
            statistics = production_unit["statistics"]
            total_produced += statistics["mass"]

        summary_data = [
            ["Production Units", str(len(production_units))],
            ["Segments", str(len(segments))],
            ["Average Production Rate", f"{monthly_rate:.2f} t/h"],
            ["Total Produced", f"{total_produced:.2f} t"],

        ]

        summary_table = Table(
            summary_data,
            colWidths=[70 * mm, 40 * mm],
        )

        summary_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    LIGHTGREY,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    GREY,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ])
        )

        elements.append(summary_table)


        # --------------------------------------------------
        # Production units / batches
        # --------------------------------------------------

        elements.append(
            Paragraph(
                "Production Units",
                styles["Heading2"],
            )
        )

        production_rows = [
            [
                "Production ID",
                "Recipe",
                "Produced (+ Adds)",
                "Runtime",
                "Rate",
                "Additives",
            ]
        ]

        for production_unit in production_units:

            statistics = production_unit["statistics"]

            additives = statistics["additives"]

            additive_lines = []

            for index in range(1, 6):

                additive = additives[f"add{index}"]

                additive_lines.append(
                    f"Add. {index}: "
                    f'{additive["mass"]:.2f} t '
                    f'({additive["percent"]:.2f}%)'
                )

                additives_text = "<br/>".join(
                    additive_lines
                )

            production_rows.append([
                production_unit["prodId"],
                production_unit["recipeName"],
                f'{statistics["mass"]:.2f} ({statistics["totalInclAdditives"]:.2f}) t',
                f'{statistics["hours"]:.2f} h',
                f'{statistics["rate"]:.2f} t/h',
                Paragraph(
                    additives_text,
                    styles["BodyText"],
                ),
            ])

        production_table = Table(
            production_rows,
            colWidths=[
                32 * mm,
                28 * mm,
                32 * mm,
                22 * mm,
                24 * mm,
                50 * mm,
            ],
            repeatRows=1,
        )

        production_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    LIGHTGREY,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    GREY,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
            ])
        )

        elements.append(production_table)

        elements.append(
            Spacer(1, 8 * mm)
        )

        # --------------------------------------------------
        # Segments
        # --------------------------------------------------

        elements.append(
            Paragraph(
                "Segments",
                styles["Heading2"],
            )
        )

        segment_rows = [
            [
                "Segment ID",
                "Production ID",
                "Start",
                "Stop",
                "Runtime",
                "Mass",
            ]
        ]

        for segment in segments:

            days = segment["runTime"] / (3600)

            segment_rows.append([
                segment["segmentId"],
                segment["prodId"],
                segment["startTime"],
                segment["stopTime"],
                f'{days:.1f} h',
                f'{segment["massTotal"]:.2f} t',
            ])

        segment_table = Table(
            segment_rows,
            repeatRows=1,
        )

        segment_table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    LIGHTGREY,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    GREY,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
            ])
        )

        elements.append(segment_table)

        document.build(elements)

        return buffer.getvalue()