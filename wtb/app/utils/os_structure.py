import datetime

import pandas as pd

from app.data_structures.taskboard import TaskBoard


def get_week_dates_from_today(today: datetime.date, weekday: int) -> list[datetime.date]:
    # Find the start of the week (Monday)
    start_of_week = today - datetime.timedelta(days=weekday - 1)

    # Generate all dates in the week
    return [start_of_week + datetime.timedelta(days=i) for i in range(7)]


def save_weekly_taskboards(weekly_taskboards: list[TaskBoard], num_weekdays: int = 7, verbose: bool = True) -> None:
    """
    Saves the weekly TaskBoards to a single Excel file. Where each sheet is a TaskBoard of the week.

    :param weekly_taskboards: A list of TaskBoard objects. Ordered by day of the week.
    :param num_weekdays: (optional) The number of weekdays in the week. Default is 7.
    :param verbose: (optional) A boolean to print information about the saving process. Default is True.
    """
    today = datetime.date.today()
    year, week, weekday = today.isocalendar()
    week_dates = get_week_dates_from_today(today, weekday)

    filename = f"data/results/XLSX/Taskboard_{year}_Week_{week}.xlsx"

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        for i in range(num_weekdays):
            if weekly_taskboards[i] is None:
                if verbose:
                    print(f"The {i + 1}th TaskBoard of the week was EMPTY and NOT saved.")
                continue

            name = str(week_dates[i])
            df = weekly_taskboards[i].to_dataframe()
            df.to_excel(writer, sheet_name=name, index=False)

            if verbose:
                print(f"Saved the {i + 1}th TaskBoard of the week as sheet: '{name}'.")
                print(f"DataFrame:\n{df}\n")

    if verbose:
        print(f"Saved the weekly TaskBoards to '{filename}'.\n")


def get_html_save_path() -> str:
    """
    A path for saving the current week's HTML file from Altiplan.

    :return: A string with the path to save the HTML file.
    """
    year, week, _ = datetime.date.today().isocalendar()

    dir_path = "data/html/"

    return dir_path + f"ALTIPLAN_{year}_Week_{week}.html"


def get_current_stuefordeling_path() -> str:
    """
    A path for the current (when run) week's Stuefordeling Excel file.

    :return: A string with the path to the Stuefordeling Excel file.
    """
    year, week, _ = datetime.date.today().isocalendar()

    dir_path = "data/stuefordelinger/"

    return dir_path + f"STUE-AMBULATORIEOVERSIGT UGE {week}-{year}.xlsx"
