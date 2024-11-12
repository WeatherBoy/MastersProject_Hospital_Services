import os

import toml
from bs4 import BeautifulSoup

from app.utils.data_formatting import soup_to_weekly_taskboards
from app.utils.os_structure import get_html_save_path
from tests.utils.valid_cells import valid_name_cell, valid_time_cell


def test_valid_formatting_from_html():
    """ """
    config = toml.load("config.toml")

    # Load the HTML from the file
    path_html = get_html_save_path()

    assert os.path.exists(path_html), f"The plan for this week hasn't been scraped. Path: {path_html}"

    with open(path_html, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    weekly_taskboards = soup_to_weekly_taskboards(soup, config)
    weekly_dataframes = [tb.to_dataframe() for tb in weekly_taskboards if tb is not None]  # <-- TaskBoard might be none - HosInfo shennanigans

    # Check if the cells are formatted correctly
    for indx, df in enumerate(weekly_dataframes):
        for column in df.columns:
            if column == "Nurse":
                for name in df[column]:
                    assert valid_name_cell(name, config), f"Invalid name: {name} - in dataframe {indx + 1}"
            elif column == "Time":
                for time in df[column]:
                    assert valid_time_cell(time), f"Invalid time: {time} - in dataframe {indx + 1}"
            else:
                continue
