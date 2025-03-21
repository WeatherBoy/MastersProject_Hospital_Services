def rygvagt_mandatory_leave_info(num_days: int, all_days: list[int]) -> tuple[dict[int, int], list[dict[str, int]]]:
    """
    Utility for the constraint regarding how the 'rygvagt' task is scheduled on weekends.

    :param num_days: Number of days in the scheduling horizon.
    :param all_days: List of all days in the scheduling horizon.

    :return: Tuple of a dictionary mapping each day to the day of the week (0=Monday, ..., 6=Sunday)
    and a list of dictionaries with information about the weekend constraints.
    """
    # NOTE: This is horrendous and need to be fixed:
    # Offset to align index 0 with Wednesday (0=Monday, ..., 6=Sunday)
    day_offset = 2

    # Map each day to the day of the week (0=Monday, ..., 6=Sunday), with offset
    day_of_week = {day: (day + day_offset) % 7 for day in all_days}

    # Identify weekends and their corresponding Mondays
    weekend_info = []
    for day in all_days:
        if day_of_week[day] == 5:  # Saturday
            saturday = day
            sunday = day + 1 if day + 1 < num_days else None
            monday_before = day - 5 if day - 5 >= 0 else None  # Previous Monday
            monday_after = day + 2 if day + 2 < num_days else None  # Next Monday

            if sunday is not None and day_of_week[sunday] == 6:
                weekend_info.append({"saturday": saturday, "sunday": sunday, "monday_before": monday_before, "monday_after": monday_after})

    return day_of_week, weekend_info
