import pandas as pd
from scheduling.app.data_structures.agent import Agent


def read_tasks():
    pass


def read_agents(path: str) -> list[Agent]:
    """ """

    # Read the Excel file, without enumerating the rows, first column as index
    df = pd.read_excel(path, index_col=0)

    agents = []
    for indx, row in df.iterrows():
        agent = Agent(name=indx)
        qualifications = {}
        for task in df.columns[1:]:
            if row[task].lower() == "x":
                qualifications[task] = True
            else:
                qualifications[task] = False

        agent.add_qualifications(qualifications)
        agents.append[agent]


def read_rolling_chart():
    """
    Preferences for 'Rygvagten'.
    """
