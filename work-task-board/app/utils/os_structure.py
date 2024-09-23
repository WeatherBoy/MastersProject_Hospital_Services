import datetime
import os
from data_structures.TaskBoard import TaskBoard


def get_week_dates_from_today(today: datetime.date, weekday: int) -> list[datetime.date]:
    # Find the start of the week (Monday)
    start_of_week = today - datetime.timedelta(days=weekday - 1)

    # Generate all dates in the week
    return [start_of_week + datetime.timedelta(days=i) for i in range(7)]


def save_weekly_taskboards(weekly_taskboards: list[TaskBoard], num_weekdays: int = 7) -> None:
    """ """
    today = datetime.date.today()
    year, week, weekday = today.isocalendar()

    dir_path = f"results/{year}_Week_{week}/"

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    week_dates = get_week_dates_from_today(today, weekday)

    for i in range(num_weekdays):
        if weekly_taskboards[i] is None:
            print(f"The {i + 1}th TaskBoard of the week was EMPTY and NOT saved.")
            continue
        name = str(week_dates[i])
        df = weekly_taskboards[i].to_dataframe()
        df.to_csv(dir_path + name + ".csv", index=False)
        print(f"Saved {i + 1}th TaskBoard of the week succesfully as: {dir_path + name}.csv")
        print(f"DataFrame:\n{df}\n")
