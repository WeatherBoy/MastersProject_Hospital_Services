import bs4

from app.data_structures.taskboard import FunctionAssignment, TaskBoard
from app.utils.string_process import empty_cell, regex_formatting_time_name


def soup_to_weekly_taskboards(soup: bs4.BeautifulSoup, config: dict[str, any]) -> list[TaskBoard]:
    """
    This utilizes the `TaskBoard` and `FunctionAssignment` classes to create a list of `TaskBoard` objects, based on the parsed HTML content.
    This serves to yield a representation of the task board for each day of the week.

    :param soup: The parsed HTML content.

    :return: A list of `TaskBoard` objects, each representing a day of the week.
    """
    ## Preliminary ***********************************************************************************************
    # Unpack the configuration settings
    num_weekdays = config["settings"]["NUM_WEEKDAYS"]
    skipable_funcs = config["settings"]["skippable_funcs"]  # <-- A list of function indices that should be skipped.

    weekly_taskboards = [None] * num_weekdays
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

            if weekly_taskboards[day_indx] is None:
                taskboard = TaskBoard()
                weekly_taskboards[day_indx] = taskboard

            weekly_taskboards[day_indx].add_function_to_nurse(name_formatted, function_assignment)

    return weekly_taskboards
