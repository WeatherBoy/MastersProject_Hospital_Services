import re


def valid_time_cell(cell_value: str) -> bool:
    """
    Checks whether a cell value is valid for a 'Time' value.

    :param cell_value: A string that is supposed to be a split of the original cell value.
    """

    valid_symbols = [":", "-", " "]

    for char in cell_value:
        if not char.isdigit() and char not in valid_symbols:
            return False

    return True


def valid_name(name: str) -> bool:
    """
    Checks whether the name has been formatted correctly.
    By checking if the name only contains letters and valid symbols.

    :param name: A string that is supposed to be a name.
    """
    valid_symbols = [" ", "."]

    for char in name:
        if not char.isalpha() and char not in valid_symbols:
            return False
    return True


def valid_moniker(parentheses_content: str, config: dict[str, any]) -> bool:
    """
    Checks whether content in parentheses is a valid moniker.
    By going through a list of valid monikers.
    If there is no parentheses, then it is by default valid.

    :param parentheses_content: A string that is supposed to be the content of a parentheses.
    :config: A dictionary with the configuration settings.
    """
    valid_monikers = config["settings"]["valid_monikers"]

    if parentheses_content is None:
        return True
    else:
        # Detect if parentheses_content is a known moniker
        for moniker in valid_monikers:
            if moniker.lower() in parentheses_content.lower():
                return True

    return False


def valid_name_cell(cell_value: str, config: dict[str, any]) -> bool:
    """
    Checks whether a cell value is valid for a 'Name' value.

    :param cell_value: A string that is supposed to be a split of the original cell value.
    :config: A dictionary with the configuration settings.
    """
    valid_name = False

    pattern = r"^([A-Za-zÆØÅæøå]+(?:\s[A-Za-zÆØÅæøå]\.)*)\s*(?:\(([^)]+)\))?$"

    match = re.match(pattern, cell_value)
    if match:
        name = match.group(1)
        parentheses_content = match.group(2)

        return valid_name(name) and valid_moniker(parentheses_content, config)
    else:
        return False
