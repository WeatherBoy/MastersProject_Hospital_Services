import re


def str_and_non_empty(cell: str) -> bool:
    """
    Check if a cell is valid.
    """
    return type(cell) is str and cell.strip() != ""


def is_flex(function: str) -> bool:
    """
    Check if a function is a flex location.

    :param location: A string with the function.

    :return: A boolean indicating if the function is a flex location.
    """
    return "flex" in function.lower()


def strip_str(cell: str) -> str:
    """
    Strip a string of all whitespaces and make it lowercase.
    This is intended to be used for comparison purposes.

    :param cell: A string.

    :return: A string with all whitespaces removed and in all lowercase.
    """
    return cell.lower().replace(" ", "")


def handle_initials(initials: str, config: dict[str, any]) -> str:
    """
    Sometimes the initials aren't initials, but in fact monikers instead.
    This function handles those edge cases.

    :param initials: A string of initials.

    :return: A string of initials formatted as initials or a moniker.
    """
    edge_case_last_names = config["settings"]["valid_monikers"]

    formatted_initials = " ".join([initial.upper() + "." for initial in initials])  # <-- add a period after each letter

    for edge_case_name in edge_case_last_names:
        if edge_case_name in initials.lower():
            formatted_initials = f"({initials.capitalize()})"
            break

    return formatted_initials


def format_name(name: str, config: dict[str, any]) -> str:
    """
    Split name into first name and initials and format and capitalize them.
    """
    if "_" in name:
        first_name, initials = name.split("_", 1)  # <-- Split string into first name and initials

        formatted_first_name = first_name.capitalize()

        formatted_initials = handle_initials(initials, config)

        return f"{formatted_first_name} {formatted_initials}"

    else:
        return name.capitalize()


def regex_formatting_time_name(cell_split: str, config: dict[str, any]) -> tuple[str, dict[str, str]] | tuple[None, None]:
    """
    NOTE: This is really just in the attempt of accomplishing a MVP.
    I don't believe regex formatting is very robust, but the alternative was using an NLP,
    and that would be complete overkill.

    This function is supposed to take a string and split it into `name_formatted`, "Time", and "Extra".

    :param cell_split: A string that is supposed to be a split of the original cell value.

    :return: The `name_formatted` (a string) and a dictionary with the keys "Time", and "Extra" or None if an error occured.
    """
    pattern = r"^([^\s(]+(?:_[^\s(]+)?)\s*(?:\(([^)]+)\))?\s*(.*)$"

    match = re.match(pattern, cell_split)
    if match:
        name_raw = match.group(1).strip()
        time_slot = match.group(2) or ""
        extra_info = match.group(3).strip()
        time_slot = time_slot if time_slot else None  # <-- If time_slot is an empty string, set it to None
        extra_info = extra_info if extra_info else None  # <-- If extra_info is an empty string, set it to None

        name_formatted = format_name(name_raw, config)

        return name_formatted, {"Time": time_slot, "Extra": extra_info}
    else:
        # NOTE: This is poor error handling - placeholder
        # Maybe I have decided, that this is adequate error handling
        return None, None


def add_stue(location: str | int) -> str:
    """
    Add "Stue" to the location if it's JUST a numer.

    :param location: A string or integer with the location.

    :return: A string with "Stue" added to the location if it's just a number.
    """
    if type(location) is int or location.replace(" ", "").isnumeric():
        location = f"Stue {location}"

    return location
