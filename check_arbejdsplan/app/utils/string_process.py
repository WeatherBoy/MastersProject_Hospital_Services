import datetime
import re

from app import INVALID_TASKS


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


def regex_filtering(cell: str | None) -> bool:
    """
    Check whether cell contains timeslot information. Returns true if it doesn't, false otherwise.
    NOTE: This might be a bit SUS.. be aware.

    :param cell: A cell from the lejeplan, representing a task.

    :return: A boolean indicating whether the task is valid.
    """
    valid_task_pattern = r"^(?=.*[A-Za-zÆØÅæøå])[A-Za-zÆØÅæøå0-9 .,'/-]+$"
    valid = re.match(valid_task_pattern, cell)

    return valid


def extract_task(cell: str, config: dict[str, any] = None) -> list[str]:
    """
    Extract tasks from a cell in the arbejdsplan. Optionally filter tasks using a regex pattern.
    NOTE: cells in the arbejdsplan may be separated into multiple tasks by '|'.

    :param cell: A cell from the arbejdsplan, representing one or multiple tasks.
    :param config: (optional) A dictionary with the configuration settings. Default is None.

    :return: A list of tasks extracted from the cell.
    """
    ## Preliminary - Unpack configurations ***********************************************************************
    # Default resolution and dpi
    enable_regex_filter = False
    enable_invalid_task_filter = False
    if config is not None:
        enable_regex_filter = config["string_processing"]["enable_regex_filter"]
        enable_invalid_task_filter = config["string_processing"]["enable_invalid_task_filter"]
    ## ***********************************************************************************************************

    tasks = cell.split("|")
    if enable_regex_filter:
        tasks = [task for task in tasks if regex_filtering(task)]
    if enable_invalid_task_filter:
        tasks = [task for task in tasks if strip_str(task) not in INVALID_TASKS]

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
            date = datetime.datetime.strptime(match.group(), "%d-%m-%Y").date()
            dates.append(date)
        else:
            raise Exception(f"`datetime.date` not found in header: {header}\nOBS: maybe check excel-file formatting!")

    return dates
