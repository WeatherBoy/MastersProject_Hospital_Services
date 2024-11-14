import pandas as pd


def write_schedule_to_excel(
    filename: str, data_path: str, assignments: list[dict[str, int | str]], agent_assignments: dict[str, int], verbose: bool = True
) -> None:
    """
    Writes the schedule and agent assignment counts to an Excel file.

    :param filename: Name of the Excel file to write to.
    :param assignments: List of assignment dictionaries with keys 'Day', 'Task' and 'Agent'.
    :param agent_assignments: Dictionary with agent names as keys and total assignments as values.
    :param verbose: (optional) If True, prints the filename. Default is True.
    """
    schedule_df = pd.read_excel(data_path, index_col=0, sheet_name="doctor_charts")
    task_df = pd.read_excel(data_path, index_col=0, sheet_name="tasks")
    task_df = task_df.drop("O-OP (tirsdag)", axis=1)

    for assignment in assignments:
        day = schedule_df.index[assignment["Day"]]
        agent = assignment["Agent"]
        task = assignment["Task"]
        if task == "O-OP (tirsdag)":
            task = "O-OP"
        schedule_df.loc[day, agent] = task
        task_df.loc[day, task] = agent

    # Create a DataFrame for agent assignments
    agent_assignments_df = pd.DataFrame(list(agent_assignments.items()), columns=["Agent", "Total Assignments"])

    # Write to Excel
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        schedule_df.to_excel(writer, sheet_name="Schedule")
        task_df.to_excel(writer, sheet_name="Task Assignments")
        agent_assignments_df.to_excel(writer, sheet_name="Agent Assignments", index=False)

    if verbose:
        print(f"Schedule and agent assignments written to {filename}")
