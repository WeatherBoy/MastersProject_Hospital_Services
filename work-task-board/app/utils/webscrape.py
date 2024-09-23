import os

import bs4
import toml

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

from utils.os_structure import get_html_save_path


def get_soup_from_altiplan(config: dict[str, any] = None) -> bs4.BeautifulSoup | None:
    """
    Uses Selenium to scrape the Altiplan website (with the configurations given by a config)
    and returns the HTML as a BeautifulSoup object.

    :param config: A dictionary containing the configurations for the scraping process.

    :return: A BeautifulSoup object containing the HTML of the Altiplan website.
    """
    # **Unpacking the config dictionary** #########################################################
    if config is None:
        config = config = toml.load("config.toml")

    SAVE_HTML = config["settings"]["save_html"]
    URL_LOGIN = config["settings"]["url_login"]
    URL_SCHEDULE = config["settings"]["url_schedule"]
    JS_ID_DEPARTMENT = config["settings"]["js_ID_department"]
    JS_ID_USERNAME = config["settings"]["js_ID_username"]
    JS_ID_PASSWORD = config["settings"]["js_ID_password"]
    JS_XPATH_UNIQE_AFTERLOGIN_ELEM = config["settings"]["js_XPATH_unique_afterlogin_elem"]
    RUN_HEADLESS = config["settings"]["run_headless"]
    ###############################################################################################

    # Get credentials from .env file
    load_dotenv()  # <-- loads the .env file

    username = os.getenv("USERID")
    password = os.getenv("PASSWORD")
    department = os.getenv("DEPARTMENT")

    # Initialize Chrome options (optional: run in headless mode)
    options = Options()
    options.headless = RUN_HEADLESS

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(URL_LOGIN)  # <-- open login page

        # Wait until the input fields are present
        wait = WebDriverWait(driver, 10)
        afd_input = wait.until(EC.presence_of_element_located((By.ID, JS_ID_DEPARTMENT)))
        brugernavn_input = driver.find_element(By.ID, JS_ID_USERNAME)
        password_input = driver.find_element(By.ID, JS_ID_PASSWORD)

        # Input your credentials
        afd_input.send_keys(department)
        brugernavn_input.send_keys(username)
        password_input.send_keys(password)

        # Submit via submit-button
        submit_button = driver.find_element(By.NAME, "submitButton")
        submit_button.click()

        # Wait for the login process to complete
        wait.until(EC.presence_of_element_located((By.XPATH, JS_XPATH_UNIQE_AFTERLOGIN_ELEM)))

        print("Login successful.")

        # Navigate to the target page
        driver.get(URL_SCHEDULE)

        # Wait until the target page loads
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Scrape the required data
        soup = bs4.BeautifulSoup(driver.page_source, "html.parser")

        if SAVE_HTML:
            path_html_output = get_html_save_path()
            with open(path_html_output, "w", encoding="utf-8") as file:
                file.write(str(soup))

    except Exception as e:
        driver.quit()
        print(f"An error occurred!!: {e}")
        return None

    finally:
        # Close the browser
        driver.quit()
        return soup
