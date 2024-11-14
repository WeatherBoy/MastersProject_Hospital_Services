import datetime
import os

from app.data_structures.taskboard import TaskBoard


def get_week_dates_from_today(today: datetime.date, weekday: int) -> list[datetime.date]:
    # Find the start of the week (Monday)
    start_of_week = today - datetime.timedelta(days=weekday - 1)

    # Generate all dates in the week
    return [start_of_week + datetime.timedelta(days=i) for i in range(7)]


def save_weekly_taskboards(weekly_taskboards: list[TaskBoard], num_weekdays: int = 7, verbose: bool = True) -> None:
    """ """
    today = datetime.date.today()
    year, week, weekday = today.isocalendar()

    dir_path = f"data/results/{year}_Week_{week}/"

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    week_dates = get_week_dates_from_today(today, weekday)

    for i in range(num_weekdays):
        if weekly_taskboards[i] is None:
            if verbose:
                print(f"The {i + 1}th TaskBoard of the week was EMPTY and NOT saved.")
            continue

        name = str(week_dates[i])
        df = weekly_taskboards[i].to_dataframe()
        df.to_excel(dir_path + name + ".xlsx", index=False, engine="openpyxl")

        if verbose:
            print(f"Saved {i + 1}th TaskBoard of the week succesfully as: {dir_path + name}.xlsx")
            print(f"DataFrame:\n{df}\n")


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
