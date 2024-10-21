import pandas as pd

from app.data_structures.agent import Agent


def str_and_x(cell: any) -> bool:
    return type(cell) is str and cell.lower() == "x"


def read_tasks(path: str) -> tuple[list[str], dict[str, list[int]]]:
    """ """

    # Read the Excel file, without enumerating the rows, first column as index
    df = pd.read_excel(path, index_col=0)

    tasks = []
    task_schedules = {}

    # Iterate through cols (tasks) in dataframe
    for task in df.columns:
        tasks.append(task)
        task_schedule = []
        for indx, day in enumerate(df.index):
            if str_and_x(df[task][day]):
                task_schedule.append(indx)
        task_schedules[task] = task_schedule

    return tasks, task_schedules


def read_agents(path: str) -> list[Agent]:
    """ """

    # Read the Excel file, without enumerating the rows, first column as index
    df = pd.read_excel(path, index_col=0)

    agents = []
    for indx, row in df.iterrows():
        agent = Agent(name=indx)
        qualifications = {}
        for task in df.columns:
            if str_and_x(row[task]):
                qualifications[task] = True
            else:
                qualifications[task] = False

        agent.add_qualifications(qualifications)
        agents.append(agent)

    return agents


def read_rolling_chart():
    """
    Preferences for 'Rygvagten'.
    """
