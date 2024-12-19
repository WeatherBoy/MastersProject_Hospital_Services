import datetime

import pandas as pd

from app import MONTHS
from app.utils.string_process import valid_task


def load_arbejdsplan_lejeplan(month: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load the arbejdsplan and lejeplan, for the given month, as pandas DataFrames.

    :param month: The month for which to load the arbejdsplan and lejeplan.

    :return: A tuple of two pandas DataFrames, representing the arbejdsplan and lejeplan, respectively.
    """
    month = month.lower()

    if month not in MONTHS:
        raise ValueError(f"Month: {month} not valid!\nMust be one of: \n{MONTHS}")

    lejeplan_path = f"data/lejeplan/{month} - lejeplan.xlsx"
    arbejdsplan_path = f"data/arbejdsplan/{month} - arbejdsplan.xlsx"

    lejeplan = pd.read_excel(lejeplan_path, header=None)  # There is only a "pseudo-header" in the lejeplan - NOTE: might be used later
    arbejdsplan = pd.read_excel(arbejdsplan_path)

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
