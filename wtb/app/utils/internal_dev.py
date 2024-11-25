import datetime

import pandas as pd

from app.data_structures.taskboard import TaskBoard
from app.utils.os_structure import get_week_dates_from_today, save_df_to_excel


def print_taskboards(weekly_taskboards: list[TaskBoard], config: dict[str, any] = None) -> None:
    """
    Meant only for internal development.

    Prints the (existing) TaskBoards in a human-readable format.

    :param weekly_taskboards: A list of TaskBoard objects. Ordered by day of the week.
    :param config: (optional) A dictionary with the configuration settings. Default is None.
    """
    weekdays = False
    if config is not None:
        weekdays = config["settings"]["WEEKDAYS"]

    for indx, taskboard in enumerate(weekly_taskboards):
        if taskboard is not None:
            if not weekdays:
                print(f"TaskBoard {indx + 1} of the week:")
            else:
                print(f"{weekdays[indx]}, TaskBoard:")
            print(taskboard.to_dataframe())


def save_functions_mismatch(weekly_taskboards: list[TaskBoard], non_matching_functions: list[list[str]]) -> None:
    """
    Meant only for internal development.

    Saves the mismatching functions between the HosInfo and Stuefordeling task boards to an Excel file.

    :param weekly_taskboards: A list of TaskBoard objects. Ordered by day of the week.
    :param non_matching_functions: A list of lists of strings. Each list contains the mismatching functions for a day.
    """
    today = datetime.date.today()
    year, week, weekday = today.isocalendar()

    filename = f"data/functions_mismatch/Functions_mismatch_{year}_Week_{week}.xlsx"

    week_dates = get_week_dates_from_today(today, weekday)
    dfs = []

    col1_id = "Alle funktioner HosInfo"
    col2_id = "Stuefordeling funktioner uden par"

    for indx, taskboard in enumerate(weekly_taskboards):
        if taskboard is not None:
            taskboard_funcs = taskboard.get_function_names()
            taskboard_funcs.sort(key=str.lower)
            stuefordeling_funcs = non_matching_functions[indx]

            if stuefordeling_funcs is not None:
                df = []

                stuefordeling_funcs.sort(key=str.lower)

                for i in range(len(taskboard_funcs)):
                    if i < len(stuefordeling_funcs):
                        df.append({col1_id: taskboard_funcs[i], col2_id: stuefordeling_funcs[i]})
                    else:
                        df.append({col1_id: taskboard_funcs[i], col2_id: None})

            dfs.append(pd.DataFrame(df))

    # Write to Excel
    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        for i, df in enumerate(dfs):
            name = str(week_dates[i])
            save_df_to_excel(df, writer, name)
