import toml
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import webbrowser

# Get URL from config file
config = toml.load("config.toml")

login_url = config["settings"]["login_url"]
schedule_url = config["settings"]["schedule_url"]
print(login_url)

load_dotenv()  # This loads the .env file

username = os.getenv("USERID")
password = os.getenv("PASSWORD")
department = os.getenv("DEPARTMENT")

# Start a session to persist cookies
session = requests.Session()

# Step 1: Get the login page
login_page = session.get(login_url)

# Step 2: Parse the page to extract CSRF token (if applicable)
soup = BeautifulSoup(login_page.text, "html.parser")

# Look for a CSRF token input field (adjust the selector as per the actual HTML structure)
csrf_token = soup.find("input", {"name": "csrf_token"})["value"] if soup.find("input", {"name": "csrf_token"}) else None

# Payload with login credentials and CSRF token (if applicable)
payload = {
    "Brugernavn": username,
    "Password": password,
    "Afd": department,
    "submit": "Log ind",
}

# If a CSRF token is present, add it to the payload
if csrf_token:
    print("CSRF token found:", csrf_token)
    payload["csrf_token"] = csrf_token

# Send the POST request to log in
login_response = session.post(login_url, data=payload, allow_redirects=True)

print(login_response.ok)
print(login_response.status_code)
print(login_response.history)

# Check if login was successful by inspecting the response
if login_response.ok:

    print("Login successful!")

    # Check cookies to see if session persists
    print(session.cookies.get_dict())

    # Now get the protected page
    response = session.get(schedule_url)

    # Save the HTML content to a file
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(response.text)

    webbrowser.open("output.html")

else:
    print("Login failed!")
