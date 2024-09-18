import toml
import re
from bs4 import BeautifulSoup

NUM_WEEKDAYS = 7
ERGO_AKTIVITETER = 65 

# Get configs from config file
config = toml.load("config.toml")
path_html_output = config["settings"]["path_html_output"]

# Load the HTML from the file
with open(path_html_output, "r", encoding="utf-8") as file:
    html_content = file.read()


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

        first_name_formatted = first_name.capitalize()

        initials_formatted = " ".join([initial.upper() + "." for initial in initials])  # <-- add a period after each letter

        return f"{first_name_formatted} {initials_formatted}"

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
        return None, None


# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")
elems = soup.find_all("div", class_="description-label")

# Print all of the element
for indx, elem in enumerate(elems):
    print(f"Day {indx + 1} of the week: \t{elem.text}")

functions = soup.find_all("div", class_="single-function")

num_functions = 0
test_indx = 0
print(f"Functions type: {type(functions)}")
print(f"Functions[{test_indx}]: {functions[test_indx].text}")
print("\n**Here comes the functions!**")
for indx, func in enumerate(functions):
    num_functions += 1
    print(f"Function {func["data-index"]}: {func.text}")
    # access "data-index" attribute of *div element* "single-function"
    data_index = func["data-index"]

assert num_functions == (int(data_index) + 1), "The number of functions does not match the (final) data-index!"

days = [None] * NUM_WEEKDAYS

data = soup.find_all("div", class_="single-description")
for indx, cell in enumerate(data):
    if empty_cell(cell.text):
        continue
    
    day_indx = indx % NUM_WEEKDAYS
    function_indx = indx // NUM_WEEKDAYS
    
    if function_indx == ERGO_AKTIVITETER:
        # Currently I skip 'Ergo aktiviteter' as, as far as I can see, they seem to be an outlier.
        # NOTE: Mention this for nurse.
        print(f"Ergo aktiviteter: {cell.text.split('\n')}")
        continue
    

    cell_splits = cell.text.split("\n")
    print(f"Cell_splits: {cell_splits}")
    for cell_split in cell_splits:
        print(cell_split, "")
        if empty_cell(cell_split):
            continue

        name_formatted, data_formatted = regex_formatting_time_name(cell_split)
        if format_name is None or data_formatted is None:
            raise Exception("Placeholder error: U done goofed, Boyoh!")

        if days[day_indx] is None:
            days[day_indx] = {name_formatted: [data_formatted]}
        else:
            if name_formatted in days[day_indx]:
                days[day_indx][name_formatted].append(data_formatted)
            else:
                days[day_indx][name_formatted] = [data_formatted]
