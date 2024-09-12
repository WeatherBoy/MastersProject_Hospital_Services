import json


def load_altiplan_cookies_headers() -> tuple[dict, dict]:
    secrets = None

    with open("secrets.json", "r") as file:
        secrets = json.load(file)

    cookies = secrets["ALTIPLAN_COOKIES"]
    headers = secrets["ALTIPLAN_HEADERS"]
    return cookies, headers
