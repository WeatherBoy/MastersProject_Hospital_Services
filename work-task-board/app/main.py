import toml
import requests
from utils.load_secrets import load_altiplan_cookies_headers
from dotenv import load_dotenv
from bs4 import BeautifulSoup


if __name__ == "__main__":
    # Get configs from config file
    config = toml.load("config.toml")
    url_schedule = config["settings"]["url_schedule"]
    path_html_output = config["settings"]["path_html_output"]
    NUM_WEEKDAYS = config["settings"]["NUM_WEEKDAYS"]
    ERGO_AKTIVITETER = config["settings"]["ERGO_AKTIVITETER"]
    BARN_SYG_AND_FERIE = config["settings"]["BARN_SYG_AND_FERIE"]

    # Get cookies and headers from .env file
    load_dotenv()  # Lads the .env file
    cookies, headers = load_altiplan_cookies_headers()

    response = requests.get(url_schedule, cookies=cookies, headers=headers)

    # NOTE: NOT FINAL! - Save the HTML content to a file
    with open(path_html_output, "w", encoding="utf-8") as file:
        file.write(response.text)

    # Parse the page content
    soup = BeautifulSoup(response.content, "html.parser")

    """
    data = soup.find_all("div", class_="single-description")
    print("**Here comes the data!**")
    for indx, item in enumerate(data):
        if item.text == "":  # <-- Empty string
            print(f"Item {indx}: No data!")
        elif item.text.strip() == "":  # <-- Whitespace
            print(f"Item {indx}:  Whitespace!")
        else:
            print(f"Item {indx}: {item.text}")
    """
