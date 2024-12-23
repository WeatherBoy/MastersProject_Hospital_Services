import datetime

import pandas as pd

from app import MONTHS
from app.utils.string_process import extract_dates, extract_task, valid_task


def load_arbejdsplan_lejeplan(month: str) -> tuple[pd.DataFrame, pd.ExcelFile]:
    """
    Load the arbejdsplan and lejeplan, for the given month, as pandas DataFrames.

    :param month: The month for which to load the arbejdsplan and lejeplan.

    :return: A tuple of a pandas DataFrame (lejeplan) and a pandas ExcelFile (arbejdsplan).
    """
    month = month.lower()

    if month not in MONTHS:
        raise ValueError(f"Month: {month} not valid!\nMust be one of: \n{MONTHS}")

    lejeplan_path = f"data/lejeplan/{month} - lejeplan.xlsx"
    arbejdsplan_path = f"data/arbejdsplan/{month} - arbejdsplan.xlsx"

    lejeplan = pd.read_excel(lejeplan_path, header=None)  # There is only a "pseudo-header" in the lejeplan - NOTE: might be used later
    arbejdsplan = pd.ExcelFile(arbejdsplan_path)

    return lejeplan, arbejdsplan


def lejeplan_daily_tasks_lists(lejeplan: pd.DataFrame) -> list[list[str]]:
    """ """
    start_row = 1  # <-- Skip the first row (it is a pseudo-header)
    start_col = 4  # <-- Skip 'day' + 'date' + 'optional week' + "undv"?? (NOTE: "undv" always two down from week numeration)

    table_df = lejeplan.iloc[start_row:, start_col:]

    tasks_matrix = []
    for row in table_df.iterrows():
        tasks_list = [task for task in row[1] if valid_task(task)]
        tasks_matrix.append(tasks_list)

    return tasks_matrix


def lejeplan_days_ordered(lejeplan: pd.DataFrame) -> list[datetime.date]:
    """
    Get the days in the lejeplan, ordered by date, corresponding to the tasks in the lejeplan.

    :param lejeplan: A pandas DataFrame representing the lejeplan.

    :return: A list of datetime.date objects, representing the days in the lejeplan.
    """
    start_row = 1  # <-- Skip the first row (it is a pseudo-header)
    start_col = 1  # <-- Skip 'day' - start at 'date'

    days = lejeplan.iloc[start_row:, start_col]
    days_ordered = [day.date() for day in days]

    return days_ordered


def arbejdsplan_daily_tasks_lists(arbejdsplan: pd.ExcelFile) -> list[list[str]]:
    """
    Extract the daily tasks from the arbejdsplan.

    :param arbejdsplan: A pandas ExcelFile representing the arbejdsplan.

    :return: A list of lists of tasks, where each list represents the tasks for a given day.
    """
    tasks_matrix = []
    for sheet in arbejdsplan.sheet_names:
        df = arbejdsplan.parse(sheet)
        for row in df.iterrows():
            # exctract_task returns a list, so we need to sum the lists to get a single list of tasks
            tasks_matrix.append(sum([extract_task(task) for task in row[1]], []))  # <-- second param, "[ ]"", is the initial value

    return tasks_matrix


def arbejdsplan_days_ordered(arbejdsplan: pd.ExcelFile) -> list[datetime.date]:
    """
    Get the days from each sheet of the arbejdsplan, corresponding to the tasks_lists.

    :param arbejdsplan: A pandas ExcelFile representing the arbejdsplan.

    :return: A list of datetime.date objects, representing the days in the arbejdsplan.
    """
    days_ordered = []

    for sheet in arbejdsplan.sheet_names:
        df = arbejdsplan.parse(sheet)

        sheet_header = list(df.columns.values)
        sheet_header.pop(0)  # <-- Remove the first column, which is the 'Navn' column

        dates = extract_dates(sheet_header)
        days_ordered += dates

    return days_ordered


def lejeplan_dict_with_date_keys(lejeplan: pd.DataFrame) -> pd.DataFrame:
    """
    Convert the lejeplan to a dictionary, with date keys and a list of daily tasks as values.

    :param lejeplan: A pandas DataFrame representing the lejeplan.

    :return: Dict with 'date' keys and 'list of tasks' values.
    """
    tasks_matrix = lejeplan_daily_tasks_lists(lejeplan)
    days_ordered = lejeplan_days_ordered(lejeplan)

    lejeplan_dict = {date: tasks for date, tasks in zip(days_ordered, tasks_matrix)}

    return lejeplan_dict


def arbejdsplan_dict_with_date_keys(arbejdsplan: pd.ExcelFile) -> dict[datetime.date, list[str]]:
    """
    Convert the arbejdsplan to a dictionary, with date keys and a list of daily tasks as values.

    :param arbejdsplan: A pandas DataFrame representing the arbejdsplan.

    :return: Dict with 'date' keys and 'list of tasks' values.
    """
    tasks_matrix = arbejdsplan_daily_tasks_lists(arbejdsplan)
    days_ordered = arbejdsplan_days_ordered(arbejdsplan)

    arbejdsplan_dict = {date: tasks for date, tasks in zip(days_ordered, tasks_matrix)}

    return arbejdsplan_dict
