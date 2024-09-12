import json


def load_altiplan_cookies_headers():
    """ """
    secrets = None

    with open("secrets.json", "r") as file:
        secrets = json.load(file)

    cookies = secrets["ALTIPLAN_COOKIES"]
    headers = secrets["ALTIPLAN_HEADERS"]
    return cookies, headers
