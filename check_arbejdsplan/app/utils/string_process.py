import datetime
import re

import pandas as pd


def str_and_non_empty(cell: str) -> bool:
    """
    Check if a cell is valid.
    """
    return type(cell) is str and cell.strip() != ""


def strip_str(cell: str) -> str:
    """
    Strip a string of all whitespaces and make it lowercase.
    This is intended to be used for comparison purposes.

    :param cell: A string.

    :return: A string with all whitespaces removed and in all lowercase.
    """
    return cell.lower().replace(" ", "")


def valid_task(cell: str | None) -> bool:
    """
    Check if a task is valid. Not none and not empty.

    :param cell: A cell from the lejeplan, representing a task.

    :return: A boolean indicating whether the task is valid.
    """
    return pd.notna(cell) and str_and_non_empty(cell)


def extract_task(cell: str) -> list[str]:
    """
    Extract tasks from a cell in the arbejdsplan.
    NOTE: cells in the arbejdsplan may be separated into multiple tasks by '|'.

    :param cell: A cell from the arbejdsplan, representing one or multiple tasks.

    :return: A list of tasks extracted from the cell.
    """
    tasks = cell.split("|")
    tasks = [task for task in tasks if valid_task(task)]

    return tasks


def extract_dates(headers: list[str]) -> list[datetime.date]:
    """
    Extract the `datetime.date`s from the headers of the arbejdsplan.
    Perform a regex search for a `datetime.date` in each header.

    :param headers: The headers of the arbejdsplan, containing the dates.

    :return: A list of `datetime.date` objects representing the dates in the header.
    """
    date_pattern = r"\d{2}-\d{2}-\d{4}"

    dates = []
    for header in headers:
        match = re.search(date_pattern, header)
        if match:
            date = datetime.strptime(match.group(), "%d-%m-%Y").date()
            dates.append(date)
        else:
            raise Exception(f"`datetime.date` not found in header: {header}\nOBS: maybe check excel-file formatting!")

    return date
