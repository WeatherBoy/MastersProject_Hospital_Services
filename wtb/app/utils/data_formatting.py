import bs4
import pandas as pd

from app.data_structures.taskboard import FunctionAssignment, TaskBoard
from app.utils.os_structure import get_current_stuefordeling_path
from app.utils.string_process import is_flex, regex_format_flex, regex_formatting_time_name, str_and_non_empty, strip_str


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
        if cell.text.strip() == "":
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
            if cell_split.strip() == "":
                continue

            name_formatted, data_formatted = regex_formatting_time_name(cell_split, config)
            if name_formatted is None or data_formatted is None:
                raise Exception(
                    "If `regex_formatting_time_name( )` returns None, then there is no match for the regex pattern. You should update approach."
                )

            function_assignment = FunctionAssignment(
                name=functions[function_indx].text,
                time=data_formatted["Time"],
                extras=data_formatted["Extra"],
            )

            if weekly_taskboards[day_indx] is None:
                taskboard = TaskBoard()
                weekly_taskboards[day_indx] = taskboard

            weekly_taskboards[day_indx].add_function_to_nurse(name_formatted, function_assignment)

    return weekly_taskboards


def update_taskboards_with_stuefordeling(weekly_taskboards: list[TaskBoard]) -> tuple[list[TaskBoard], list[list[str]]]:
    """
    Make a new list of `TaskBoard` objects, where the functions are updated with the information from the stuefordeling.

    :param weekly_taskboards: A list of `TaskBoard` objects, each representing a day of the week.

    :return: A list of `TaskBoard` objects, each representing a day of the week, with updated function assignments.
    """
    # This initializations makes these None, if there is no data for the day. It is nicer than, say having
    # an empty list, at a random index.
    updated_weekly_taskboards = [None] * len(weekly_taskboards)
    non_matching_functions = [None] * len(weekly_taskboards)

    stuefordeling_path = get_current_stuefordeling_path()

    # Read in the file, skipping the first row
    df = pd.read_excel(stuefordeling_path, sheet_name="Læge", skiprows=1)

    # Loop through columns in pairs
    # `range(1, df.shape[1], 2)` <- Starts at 1, ends at the last column, stepsize 2: (1, 3, 5, ...)
    for indx, col in enumerate(range(1, df.shape[1], 2)):
        taskboard = weekly_taskboards[indx]
        if taskboard is None:
            continue
        flex_dict = {}
        function_names = taskboard.get_function_names()
        function_names_stripped = [strip_str(name) for name in function_names]

        # Column names
        day_column = df.columns[col]
        doctor_column = df.columns[col + 1]

        # Loop through each row in this 'Dag' and 'Læge' pair
        for _, row in df.iterrows():
            location = str(row.iloc[0]).strip()  # The first column as location
            function = row[day_column] if str_and_non_empty(row[day_column]) else None
            doctor = row[doctor_column] if str_and_non_empty(row[doctor_column]) else None

            # Only add rows with a valid function (ignore empty cells)
            if pd.notna(function):
                function_stripped = strip_str(function)

                if is_flex(function):
                    flex_location = location  # <-- If the current function is 'flex', then the current location is a flex location
                    flex_locations = regex_format_flex(function)
                    for locations in flex_locations:
                        flex_dict[locations] = flex_location

                elif function_stripped not in function_names_stripped:  # <-- NOTE: make search on stripped, lower-case name
                    if non_matching_functions[indx] is None:
                        non_matching_functions[indx] = []
                    non_matching_functions[indx].append(function)

                else:
                    function_indx = function_names_stripped.index(function_stripped)  # <-- NOTE: find corresponding index, use for update
                    function_name = function_names[function_indx]
                    taskboard.update_function_assignments(function_name=function_name, location=location, doctor=doctor)

        taskboard.add_flex(flex_dict)
        updated_weekly_taskboards[indx] = taskboard

    return updated_weekly_taskboards, non_matching_functions


def flex_to_stue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a DataFrame and moves the data from the "Flexstue" column to the "Stue" column.
    This is in the interest of a less cluttered visualisation.

    :param df: A pandas DataFrame representing the final visualisation.

    :return: A pandas DataFrame with the Flexstue data moved to the Stue column.
    """
    if "Stue" in df.columns and "Flexstue" in df.columns:
        df["Stue"] = df.apply(
            lambda row: f"{row['Stue']} (Flex {row['Flexstue']})".strip(", ") if str_and_non_empty(row["Flexstue"]) else row["Stue"],
            axis=1,
        )

        # Now that it is redundant, drop the "Flexstue" colum
        df.drop(columns=["Flexstue"], inplace=True)

    return df


def timeslot_tasks_to_bottom(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a DataFrame and cleans and moves the functions with timeslots to the bottom of the DataFrame.

    :param df: A pandas DataFrame representing the final visualisation.

    :return: A pandas DataFrame with the functions with timeslots moved to the bottom.
    """
    pattern = r"\b\d{1,2}:\d{2}\b"  # Regex pattern to identify timeslots

    # Define the list of columns to clear (all columns except "Navn" and "Funktion")
    columns_to_clear = [col for col in df.columns if col not in ["Navn", "Funktion"]]

    # Clean the rows identified as `timeslot_rows` by clearing all columns except "Navn" and "Funktion"
    df.loc[df["Funktion"].str.contains(pattern, na=False, regex=True), columns_to_clear] = ""

    # Identify rows with timeslots in the "Funktion" column
    timeslot_rows = df[df["Funktion"].str.contains(pattern, na=False, regex=True)]
    non_timeslot_rows = df[~df["Funktion"].str.contains(pattern, na=False, regex=True)]

    # Reorganize DataFrame: first rows without timeslots, then rows with timeslots
    reorganized_df = pd.concat([non_timeslot_rows, timeslot_rows])

    return reorganized_df


def make_df_ready_for_visualisation(
    df: pd.DataFrame, rename_headers: bool = True, join_flex_stue: bool = True, move_time_funcs: bool = True
) -> pd.DataFrame:
    """
    Takes a DataFrame and prepares it for visualisation by renaming columns, moving Flexstue data, and cleaning functions with timeslots.
    NOTE: This is all stuff that should be done prior to visualisation, but shouldn't alter the data itself.

    :param df: A pandas DataFrame representing the final visualisation.
    :param rename_headers: (optional) A boolean to rename the headers of the DataFrame. Default is True.
    :param join_flex_stue: (optional) A boolean to move the Flexstue data to the Stue column. Default is True.
    :param move_time_funcs: (optional) A boolean to move and clean functions with timeslots to the bottom of the DataFrame. Default is True.

    :return: A pandas DataFrame ready for visualisation.
    """
    if rename_headers:
        # Dictionary for declaring the headers of the DataFrame (column names)
        header_dict = {
            "Nurse": "Navn",
            "Function": "Funktion",
            "Location": "Stue",
            "Time": "Mødetid",
            "Doctor": "Læge",
            "Extras": "Bemærkninger",
            "Flex": "Flexstue",
        }
        df.rename(columns=header_dict, inplace=True)

    if join_flex_stue:
        df = flex_to_stue(df)

    if move_time_funcs:
        df = timeslot_tasks_to_bottom(df)

    return df
