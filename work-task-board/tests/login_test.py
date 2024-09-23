import toml
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os

SAVE_ALTIPLAN_AS_HTML = True
RUN_IN_HEADLESS_MODE = True  # for performance


def get_html_save_path() -> str:
    year, week, _ = datetime.date.today().isocalendar()

    dir_path = f"data/html/"

    return dir_path + f"ALTIPLAN_{year}_Week_{week}.html"


if __name__ == "__main__":
    # Get configs from config file
    config = toml.load("config.toml")
    url_login = config["settings"]["url_login"]
    url_schedule = config["settings"]["url_schedule"]
    js_ID_department = config["settings"]["js_ID_department"]
    js_ID_username = config["settings"]["js_ID_username"]
    js_ID_password = config["settings"]["js_ID_password"]
    js_XPATH_unique_post_login_elem = config["settings"]["js_XPATH_unique_post_login_elem"]

    # Get credentials from .env file
    load_dotenv()  # This loads the .env file

    username = os.getenv("USERID")
    password = os.getenv("PASSWORD")
    department = os.getenv("DEPARTMENT")

    # Initialize Chrome options (optional: run in headless mode)
    options = Options()
    options.headless = True if RUN_IN_HEADLESS_MODE else False

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url_login)  # <-- open login page

        # Wait until the input fields are present
        wait = WebDriverWait(driver, 10)
        afd_input = wait.until(EC.presence_of_element_located((By.ID, js_ID_department)))
        brugernavn_input = driver.find_element(By.ID, js_ID_username)
        password_input = driver.find_element(By.ID, js_ID_password)

        # Input your credentials
        afd_input.send_keys(department)
        brugernavn_input.send_keys(username)
        password_input.send_keys(password)

        # Submit via submit-button
        submit_button = driver.find_element(By.NAME, "submitButton")
        submit_button.click()

        # Wait for the login process to complete
        wait.until(EC.presence_of_element_located((By.XPATH, js_XPATH_unique_post_login_elem)))

        print("Login successful.")

        # Navigate to the target page
        driver.get(url_schedule)

        # Wait until the target page loads
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Scrape the required data
        soup = BeautifulSoup(driver.page_source, "html.parser")

        if SAVE_ALTIPLAN_AS_HTML:
            path_html_output = get_html_save_path()
            with open(path_html_output, "w", encoding="utf-8") as file:
                file.write(str(soup))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()
