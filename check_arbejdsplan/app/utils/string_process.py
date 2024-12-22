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
