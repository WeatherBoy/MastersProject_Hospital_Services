import pandas as pd

from app.utils.string_process import str_and_non_empty


def flex_to_stue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges the data from the "Flexstue" column into the "Stue" column for a cleaner visualization.

    If the "Stue" column contains None or is empty, it is treated as an empty string during the merge.
    If "Flexstue" contains valid data, it is appended to the "Stue" column in the format "Stue (Flex Flexstue)".
    Otherwise, the "Stue" column remains unchanged or is set to an empty string if originally None.

    :param df: A pandas DataFrame representing the final visualisation.

    :return: A pandas DataFrame with the "Flexstue" data merged into the "Stue" column, and the "Flexstue" column removed.
    """
    if "Stue" in df.columns and "Flexstue" in df.columns:
        df["Stue"] = df.apply(
            lambda row: f"{row['Stue'] or ''} (Flex {row['Flexstue']})".strip(", ")
            if str_and_non_empty(row["Flexstue"])
            else (row["Stue"] or ""),
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
