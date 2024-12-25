import datetime


def check_arbejdsplan_with_lejeplan(
    lejeplan_dict: dict[datetime.date, list[str]],
    arbejdsplan_dict: dict[datetime.date, list[str]],
) -> bool:
    """
    Given two dicts with keys dates and values lists of tasks on that date,
    check that all tasks present in the Lejeplan are included in the Arbejdsplan.

    """
    arbejdsplan_valid = True

    arbejdsplan_dates = arbejdsplan_dict.keys()

    for date in lejeplan_dict.keys():
        if date not in arbejdsplan_dates:
            print(f"Date {date} not found in Arbejdsplan.")
            arbejdsplan_valid = False
            return arbejdsplan_valid

        lejeplan_tasks = lejeplan_dict[date]
        arbejdsplan_tasks = arbejdsplan_dict[date]

        for task in lejeplan_tasks:
            if task not in arbejdsplan_tasks:
                print(f"Task '{task}' not found in Arbejdsplan for date {date}.")
                arbejdsplan_valid = False

    return arbejdsplan_valid
