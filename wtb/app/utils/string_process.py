import re

import bs4

from app.data_structures.taskboard import FunctionAssignment, TaskBoard


def empty_cell(cell_value: str) -> bool:
    """
    Check if a cell is empty/ only contains whitespace.
    """
    return cell_value == "" or cell_value.strip() == ""


def handle_initials(initials: str, config: dict[str, any]) -> str:
    """
    Sometimes the initials aren't initials, but in fact monikers instead.
    This function handles those edge cases.

    :param initials: A string of initials.

    :return: A string of initials formatted as initials or a moniker.
    """
    edge_case_last_names = config["settings"]["valid_monikers"]

    formatted_initials = " ".join([initial.upper() + "." for initial in initials])  # <-- add a period after each letter

    for edge_case_name in edge_case_last_names:
        if edge_case_name in initials.lower():
            formatted_initials = f"({initials.capitalize()})"
            break

    return formatted_initials


def format_name(name: str, config: dict[str, any]) -> str:
    """
    Split name into first name and initials and format and capitalize them.
    """
    if "_" in name:
        first_name, initials = name.split("_", 1)  # <-- Split string into first name and initials

        formatted_first_name = first_name.capitalize()

        formatted_initials = handle_initials(initials, config)

        return f"{formatted_first_name} {formatted_initials}"

    else:
        return name.capitalize()


def regex_formatting_time_name(cell_split: str, config: dict[str, any]) -> tuple[str, dict[str, str]] | tuple[None, None]:
    """
    NOTE: This is really just in the attempt of accomplishing a MVP.
    I don't believe regex formatting is very robust, but the alternative was using an NLP,
    and that would be complete overkill.

    This function is supposed to take a string and split it into `name_formatted`, "Time", and "Extra".

    :param cell_split: A string that is supposed to be a split of the original cell value.

    :return: The `name_formatted` (a string) and a dictionary with the keys "Time", and "Extra" or None if an error occured.
    """
    pattern = r"^([^\s(]+(?:_[^\s(]+)?)\s*(?:\(([^)]+)\))?\s*(.*)$"

    match = re.match(pattern, cell_split)
    if match:
        name_raw = match.group(1).strip()
        time_slot = match.group(2) or ""
        extra_info = match.group(3).strip()
        time_slot = time_slot if time_slot else None  # <-- If time_slot is an empty string, set it to None
        extra_info = extra_info if extra_info else None  # <-- If extra_info is an empty string, set it to None

        name_formatted = format_name(name_raw, config)

        return name_formatted, {"Time": time_slot, "Extra": extra_info}
    else:
        # NOTE: This is poor error handling - placeholder
        # Maybe I have decided, that this is adequate error handling
        return None, None


def soup_to_weekly_taskboards(soup: bs4.BeautifulSoup, config: dict[str, any]) -> list[TaskBoard]:
    """
    This utilizes the `TaskBoard` and `FunctionAssignment` classes to create a list of `TaskBoard` objects, based on the parsed HTML content.
    This serves to yield a representation of the task board for each day of the week.

    :param soup: The parsed HTML content.

    :return: A list of `TaskBoard` objects, each representing a day of the week.
    """
    ## Preliminary ***********************************************************************************************
    # Unpack the configuration settings
    num_weekdays = config["settings"]["NUM_WEEKDAYS"]  # <-- A list of function indices that should be skipped.
    skipable_funcs = config["settings"]["skippable_funcs"]

    days = [None] * num_weekdays
    ## ***********************************************************************************************************

    functions = soup.find_all("div", class_="single-function")  # <-- functions (funktioner)/ rows on Altiplan
    data = soup.find_all("div", class_="single-description")  # <-- cells in the "grid" on Altiplan

    for indx, cell in enumerate(data):
        if empty_cell(cell.text):
            continue

        day_indx = indx % num_weekdays
        function_indx = indx // num_weekdays

        if functions[function_indx].text in skipable_funcs:
            # Currently I skip 'Ergo aktiviteter' as, as far as I can see, they seem to be an outlier.
            # Also, I skip 'Børn syg og ferie' as they are not relevant for the task board.
            # NOTE: Mention this for nurse.
            continue

        cell_splits = cell.text.split("\n")
        for cell_split in cell_splits:
            if empty_cell(cell_split):
                continue

            name_formatted, data_formatted = regex_formatting_time_name(cell_split, config)
            if name_formatted is None or data_formatted is None:
                raise Exception(
                    "If `regex_formatting_time_name( )` returns None, then there is no match for the regex pattern. You should update approach."
                )

            function_assignment = FunctionAssignment(
                function_name=functions[function_indx].text,
                time=data_formatted["Time"],
                extras=data_formatted["Extra"],
            )

            if days[day_indx] is None:
                taskboard = TaskBoard()
                days[day_indx] = taskboard

            days[day_indx].add_function_to_nurse(name_formatted, function_assignment)

    return days
