import re
import bs4
from data_structures.TaskBoard import TaskBoard, FunctionAssignment


def empty_cell(cell_value: str) -> bool:
    """
    Check if a cell is empty/ only contains whitespace.
    """
    return cell_value == "" or cell_value.strip() == ""


def format_name(name: str) -> str:
    """
    Split name into first name and initials and format and capitalize them.
    """
    if "_" in name:
        first_name, initials = name.split("_", 1)  # <-- Split string into first name and initials

        formatted_first_name = first_name.capitalize()

        formatted_initials = " ".join([initial.upper() + "." for initial in initials])  # <-- add a period after each letter

        return f"{formatted_first_name} {formatted_initials}"

    else:
        return name.capitalize()


def regex_formatting_time_name(cell_split: str) -> tuple[str, dict[str, str]] | tuple[None, None]:
    """
    NOTE: This is really just in the attempt of accomplishing a MVP.
    I don't believe regex formatting is very robust, but the alternative was using an NLP,
    and that would be complete overkill.

    This function is supposed to take a string and split it into `name_formatted`, "Time", and "Extra".

    :param cell_split: A string that is supposed to be a split of the original cell value.

    :return: The `name_formatted` (a string) and a dictionary with the keys "Time", and "Extra" or None if an error occured.
    """
    pattern = r"([A-Z_]+)\s*(\(([\d: -]+)\))?\s*(.*)?"

    match = re.match(pattern, cell_split)
    if match:
        name_raw = match.group(1)
        time_slot = match.group(3)
        extra_info = match.group(4)
        time_slot = time_slot if time_slot else None  # <-- If time_slot is an empty string, set it to None
        extra_info = extra_info if extra_info else None  # <-- If extra_info is an empty string, set it to None

        name_formatted = format_name(name_raw)

        return name_formatted, {"Time": time_slot, "Extra": extra_info}
    else:
        # NOTE: This is poor error handling - placeholder
        # Maybe I have decided, that this is adequate error handling
        return None, None


def soup_to_weekly_taskboards(soup: bs4.BeautifulSoup, skipable_funcs: list[int], num_weekdays: int = 7) -> list[TaskBoard]:
    """
    This utilizes the `TaskBoard` and `FunctionAssignment` classes to create a list of `TaskBoard` objects, based on the parsed HTML content.
    This serves to yield a representation of the task board for each day of the week.

    :param soup: The parsed HTML content.
    :param skipable_funcs: A list of function indices that should be skipped.
    :param num_weekdays: The number of weekdays in the schedule. Default is 7.

    :return: A list of `TaskBoard` objects, each representing a day of the week.
    """
    days = [None] * num_weekdays

    functions = soup.find_all("div", class_="single-function")
    data = soup.find_all("div", class_="single-description")

    for indx, cell in enumerate(data):
        if empty_cell(cell.text):
            continue

        day_indx = indx % num_weekdays
        function_indx = indx // num_weekdays

        if function_indx in skipable_funcs:
            # Currently I skip 'Ergo aktiviteter' as, as far as I can see, they seem to be an outlier.
            # Also, I skip 'Børn syg og ferie' as they are not relevant for the task board.
            # NOTE: Mention this for nurse.
            continue

        cell_splits = cell.text.split("\n")
        for cell_split in cell_splits:
            if empty_cell(cell_split):
                continue

            name_formatted, data_formatted = regex_formatting_time_name(cell_split)
            if format_name is None or data_formatted is None:
                raise Exception(
                    "If `regex_formatting_time_name( )` returns None, then there is no match for the regex pattern. And you should update approach."
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
