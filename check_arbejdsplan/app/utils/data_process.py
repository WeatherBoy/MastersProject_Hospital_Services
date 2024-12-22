import datetime

import pandas as pd

from app import MONTHS
from app.utils.string_process import valid_task


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
    days_ordered = [day.date() for day in days if pd.notna(day)]

    return days_ordered


def extract_task(cell: str) -> list[str]:
    """
    Extract tasks from a cell in the arbejdsplan.

    :param cell: A cell from the arbejdsplan, representing one or multiple tasks.

    :return: A list of tasks extracted from the cell.
    """
    tasks = cell.split("|")
    tasks = [task for task in tasks if valid_task(task)]

    return tasks


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
