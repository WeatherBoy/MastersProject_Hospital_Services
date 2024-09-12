import toml
import requests
from utils.load_secrets import load_altiplan_cookies_headers
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import webbrowser

# Get configs from config file
config = toml.load("config.toml")
url_schedule = config["settings"]["url_schedule"]
path_html_output = config["settings"]["path_html_output"]

# Get cookies and headers from .env file
load_dotenv()  # Lads the .env file
cookies, headers = load_altiplan_cookies_headers()

response = requests.get(url_schedule, cookies=cookies, headers=headers)

# NOTE: NOT FINAL! - Save the HTML content to a file
with open(path_html_output, "w", encoding="utf-8") as file:
    file.write(response.text)

# Parse the page content
soup = BeautifulSoup(response.content, "html.parser")

# Optionally, print the entire HTML for inspection
print(soup.prettify())
