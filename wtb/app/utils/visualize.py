import datetime
import os

import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from app.data_structures.taskboard import TaskBoard
from app.utils.os_structure import get_week_dates_from_today


def save_taskboards_as_pdf(weekly_taskboards: list[TaskBoard], config: dict[str, any] = None) -> None:
    """ """
    width, height = 1920, 1080
    header = [["Navn", "Funktion", "Lokation", "Tid", "Læge", "Extra"]]
    col_width = [220, 300, 180, 180, 130, 400]

    today = datetime.date.today()
    year, week, weekday = today.isocalendar()

    dir_path = f"data/results/PDFs/{year}_Week_{week}/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    week_dates = get_week_dates_from_today(today, weekday)

    for i, taskboard in enumerate(weekly_taskboards):
        if taskboard is None:
            print(f"The {i + 1}th TaskBoard of the week was EMPTY and NOT saved.")
            continue
        data = header + taskboard.to_matrix()

        pdf_file = f"{dir_path}{week_dates[i]}.pdf"

        doc = SimpleDocTemplate(pdf_file, pagesize=(width, height))

        # Create table with data
        table = Table(data, colWidths=col_width, rowHeights=30)

        # Define table style
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 16),  # Header font size
                    ("FONTSIZE", (0, 1), (-1, -1), 14),  # Data font size
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 15),
                    ("TOPPADDING", (0, 1), (-1, -1), 0),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
                ]
            )
        )

        # Build the PDF
        doc.build([table])

        print(f"PDF created at: {pdf_file}")


def save_taskboards_as_pdf2(weekly_taskboards: list[TaskBoard], config: dict[str, any] = None) -> None:
    """ """
    width, height = 19.2, 10.8
    header_dict = {"Nurse": "Navn", "Function": "Funktion", "Location": "Lokation", "Time": "Tid", "Doctor": "Læge", "Extras": "Extra"}
    today = datetime.date.today()
    year, week, weekday = today.isocalendar()
    week_dates = get_week_dates_from_today(today, weekday)

    dir_path = f"data/results/PNGs/{year}_Week_{week}/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for i, taskboard in enumerate(weekly_taskboards):
        if taskboard is None:
            print(f"The {i + 1}th TaskBoard of the week was EMPTY and NOT saved.")
            continue

        df = taskboard.to_dataframe()
        df.rename(columns=header_dict, inplace=True)

        # Set figure size for widescreen (e.g., 1920x1080 pixels)
        fig, ax = plt.subplots(figsize=(width, height))
        ax.axis("off")

        # Render table
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center")

        # General table styling
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.5, 1.5)

        # Header styling
        for col, _ in enumerate(df.columns):
            cell = table[0, col]
            cell.set_fontsize(14)  # Increase header font size
            cell.set_text_props(weight="bold")  # Bold font for header
            cell.set_facecolor("#d9e8fc")  # soft blue background for header
            cell.set_text_props(color="#2c3e50")  # Navy, text color for header

        # Alternate row colors for better readability
        for row in range(1, len(df) + 1):
            for col in range(len(df.columns)):
                cell = table[row, col]
                if row % 2 == 0:
                    cell.set_facecolor("#eaf3fb")  # soft pastel blue for even rows
                else:
                    cell.set_facecolor("white")  # White for odd rows

        # Save or display as an image
        plt.savefig(f"{dir_path}{week_dates[i]}.png", bbox_inches="tight", dpi=100)
        plt.close()
