import toml
import requests
import os
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import webbrowser

# Get configs from config file
config = toml.load("config.toml")
url_schedule = config["settings"]["url_schedule"]
path_html_output = config["settings"]["path_html_output"]

# Get cookies and headers from .json file
secrets = None

with open("secrets.json", "r") as file:
    secrets = json.load(file)

cookies = secrets["ALTIPLAN_COOKIES"]
headers = secrets["ALTIPLAN_HEADERS"]

response = requests.get(url_schedule, cookies=cookies, headers=headers)

# NOTE: NOT FINAL! - Save the HTML content to a file
with open(path_html_output, "w", encoding="utf-8") as file:
    file.write(response.text)

webbrowser.open(path_html_output)

# Parse the page content
soup = BeautifulSoup(response.content, "html.parser")

# Optionally, print the entire HTML for inspection
print(soup.prettify())
