import datetime
import os

import matplotlib.pyplot as plt
import pandas as pd

from app.data_structures.taskboard import TaskBoard
from app.utils.os_structure import get_week_dates_from_today
from app.utils.string_process import str_and_non_empty


def color_header(df: pd.DataFrame, table: plt.table, config: dict[str, any] = None) -> None:
    """
    Color the header of the table.

    :param df: A pandas DataFrame.
    :param table: A matplotlib table object.
    :param config: (optional) A dictionary with the configuration settings. Default is None.
    """
    ## Preliminary - Unpack configurations ***********************************************************************
    # Default configurations
    header_fontsize = 14
    background_color = "#d9e8fc"  # soft blue background for header
    font_color = "#2c3e50"  # Navy, text color for header
    if config is not None:
        header_fontsize = config["visualise"]["header_fontsize"]
        background_color = config["visualise"]["header_background_color"]
        font_color = config["visualise"]["header_font_color"]
    ## ***********************************************************************************************************

    for col, _ in enumerate(df.columns):
        cell = table[0, col]
        cell.set_fontsize(header_fontsize)
        cell.set_text_props(weight="bold")  # Bold font for header
        cell.set_facecolor(background_color)
        cell.set_text_props(color=font_color)


def color_alternating_rows(df: pd.DataFrame, table: plt.table, config: dict[str, any] = None) -> None:
    """
    Colors the rows of the table in an alternating pattern.

    :param df: A pandas DataFrame.
    :param table: A matplotlib table object.
    :param config: (optional) A dictionary with the configuration settings. Default is None.
    """
    ## Preliminary - Unpack configurations ***********************************************************************
    # Default colors
    color_even = "#eaf3fb"  # soft pastel blue for even rows
    color_odd = "white"
    if config is not None:
        color_even = config["visualise"]["color_even"]
        color_odd = config["visualise"]["color_odd"]
    ## ***********************************************************************************************************

    for row in range(1, len(df) + 1):
        for col in range(len(df.columns)):
            cell = table[row, col]
            if row % 2 == 0:
                cell.set_facecolor(color_even)
            else:
                cell.set_facecolor(color_odd)


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


def make_df_ready_for_visualisation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a DataFrame and prepares it for visualisation by renaming columns, moving Flexstue data, and cleaning functions with timeslots.
    NOTE: This is all stuff that should be done prior to visualisation, but shouldn't alter the data itself.

    :param df: A pandas DataFrame representing the final visualisation.

    :return: A pandas DataFrame ready for visualisation.
    """
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

    # Move Flexstue data to Stue
    df = flex_to_stue(df)

    # Move and clean functions with timeslots to the bottom of the DataFrame
    df = timeslot_tasks_to_bottom(df)

    return df


def save_taskboards_as_png(weekly_taskboards: list[TaskBoard], verbose: bool = True, config: dict[str, any] = None) -> None:
    """
    Saves the TaskBoards of the week as PNG images.

    :param weekly_taskboards: A list of TaskBoard objects. Ordered by day of the week.
    :param verbose: A boolean to control the print statements. Default is True.
    :param config: (optional) A dictionary with the configuration settings. Default is None.
    """
    ## Preliminary - Unpack configurations ***********************************************************************
    # Default resolution and dpi
    width, height = 19.2, 10.8
    dpi = 100
    if config is not None:
        width, height = config["visualise"]["screen_resolution"]
        width, height = width / 100.0, height / 100.0  # <-- assumes resolution is in pixels in configuration
        dpi = config["visualise"]["dpi"]
    ## ***********************************************************************************************************

    today = datetime.date.today()
    year, week, weekday = today.isocalendar()
    week_dates = get_week_dates_from_today(today, weekday)

    dir_path = f"data/results/PNGs/{year}_Week_{week}/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    for i, taskboard in enumerate(weekly_taskboards):
        if taskboard is None:
            if verbose:
                print(f"The {i + 1}th TaskBoard of the week was EMPTY and NOT saved.")
            continue

        png_file = f"{dir_path}{week_dates[i]}.png"

        df = taskboard.to_dataframe()
        df = make_df_ready_for_visualisation(df)

        fig, ax = plt.subplots(figsize=(width, height))
        ax.axis("off")

        # Render table
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc="center", loc="center")

        # General table styling
        table.auto_set_font_size(False)
        table.set_fontsize(12)
        table.scale(1.5, 1.5)

        # Header styling
        color_header(df, table, config)

        # Alternate row colors for better readability
        color_alternating_rows(df, table, config)

        # Save or display as an image
        plt.savefig(png_file, bbox_inches="tight", dpi=dpi)
        plt.close()
        if verbose:
            print(f"PNG created at: {png_file}")
