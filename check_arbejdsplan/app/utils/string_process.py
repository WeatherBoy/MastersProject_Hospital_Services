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
