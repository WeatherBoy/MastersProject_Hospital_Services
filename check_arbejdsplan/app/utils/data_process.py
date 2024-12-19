import pandas as pd

from app import MONTHS


def load_arbejdsplan_lejeplan(month: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load the arbejdsplan and lejeplan, for the given month, as pandas DataFrames.

    :param month: The month for which to load the arbejdsplan and lejeplan.

    :return: A tuple of two pandas DataFrames, representing the arbejdsplan and lejeplan, respectively.
    """
    month = month.lower()

    if month not in MONTHS:
        raise ValueError(f"Month: {month} not valid!\nMust be one of: \n{MONTHS}")

    lejeplan_path = f"data/lejeplan/{month} - lejeplan.xlsx"
    arbejdsplan_path = f"data/arbejdsplan/{month} - arbejdsplan.xlsx"

    lejeplan = pd.read_excel(lejeplan_path, header=None)  # There is only a "pseudo-header" in the lejeplan - NOTE: might be used later
    arbejdsplan = pd.read_excel(arbejdsplan_path)

    return lejeplan, arbejdsplan
