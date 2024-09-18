import re


def empty_cell(cell_value: str) -> bool:
    """
    Check if a cell is empty/ only contains whitespace.
    """
    return cell_value == "" or cell_value.strip() == ""


def format_name(name: str) -> str:
    """
    Split name into first name and initials and format and capitalize them.
    """
    if "_" in name:
        first_name, initials = name.split("_", 1)  # <-- Split string into first name and initials

        formatted_first_name = first_name.capitalize()

        formatted_initials = " ".join([initial.upper() + "." for initial in initials])  # <-- add a period after each letter

        return f"{formatted_first_name} {formatted_initials}"

    else:
        return name.capitalize()


def regex_formatting_time_name(cell_split: str) -> tuple[str, dict[str, str]] | tuple[None, None]:
    """
    NOTE: This is really just in the attempt of accomplishing a MVP.
    I don't believe regex formatting is very robust, but the alternative was using an NLP,
    and that would be complete overkill.

    This function is supposed to take a string and split it into `name_formatted`, "Time", and "Extra".

    :param cell_split: A string that is supposed to be a split of the original cell value.

    :return: The `name_formatted` (a string) and a dictionary with the keys "Time", and "Extra" or None if an error occured.
    """
    pattern = r"([A-Z_]+)\s*(\(([\d: -]+)\))?\s*(.*)?"

    match = re.match(pattern, cell_split)
    if match:
        name_raw = match.group(1)
        time_slot = match.group(3)
        extra_info = match.group(4)
        time_slot = time_slot if time_slot else None  # <-- If time_slot is an empty string, set it to None
        extra_info = extra_info if extra_info else None  # <-- If extra_info is an empty string, set it to None

        name_formatted = format_name(name_raw)

        return name_formatted, {"Time": time_slot, "Extra": extra_info}
    else:
        # NOTE: This is poor error handling - placeholder
        # Maybe I have decided, that this is adequate error handling
        return None, None
