from data_structures.task_board import TaskBoard


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
