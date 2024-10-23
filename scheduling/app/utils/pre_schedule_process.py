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


def read_agents(path: str) -> dict[str, Agent]:
    """ """

    # Read the Excel file, without enumerating the rows, first column as index
    df = pd.read_excel(path, index_col=0)

    agents = {}
    for indx, row in df.iterrows():
        agent = Agent(name=indx)
        qualifications = {}
        for task in df.columns:
            if str_and_x(row[task]):
                qualifications[task] = True
            else:
                qualifications[task] = False

        agent.add_qualifications(qualifications)
        agents[agent.name] = agent

    return agents


def read_rolling_chart(
    path: str, agents: dict[str, Agent], task_schedules: dict[str : list[int]]
) -> tuple[dict[str, Agent], dict[str : list[int]]]:
    """
    Preferences for 'Rygvagten'.
    """
    df = pd.read_excel(path, index_col=1)

    col = df.columns[1]
    schedule_horizon = len(df.index)
    task_preferences = {name: [0 for _ in range(schedule_horizon)] for name in agents.keys()}
    for indx, day in enumerate(df.index):
        agent_name = df[col][day]
        # Handling the neuro-surgeons
        if agent_name in ["TSJ", "MA", "AJ"]:
            task_schedules["Rygvagt"].remove(indx)
        else:
            task_preferences[agent_name][indx] = 1

    for agent in agents.values():
        agent.add_task_preferences(task_preferences[agent.name])

    return agents, task_schedules


def parse_agents():
    pass
