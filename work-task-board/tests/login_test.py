import toml
import requests
import json
from bs4 import BeautifulSoup
import webbrowser
import datetime

SAVE_ALTIPLAN_AS_HTML = True


def get_html_save_path() -> str:
    year, week, _ = datetime.date.today().isocalendar()

    dir_path = f"data/html/"

    return dir_path + f"ALTIPLAN_{year}_Week_{week}.html"


if __name__ == "__main__":
    # Get configs from config file
    config = toml.load("config.toml")
    url_schedule = config["settings"]["url_schedule"]

    # Get cookies and headers from .json file
    secrets = None
    with open("secrets.json", "r") as file:
        secrets = json.load(file)

    response = requests.get(url_schedule, cookies=cookies, headers=headers)

    if SAVE_ALTIPLAN_AS_HTML:
        path_html_output = get_html_save_path()
        with open(path_html_output, "w", encoding="utf-8") as file:
            file.write(response.text)
        webbrowser.open(path_html_output)

    # Parse the page content
    soup = BeautifulSoup(response.content, "html.parser")
