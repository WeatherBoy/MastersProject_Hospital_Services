import os
import time

import bs4
import toml
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait

from app.utils.os_structure import get_html_save_path


def get_soup_from_altiplan(verbose: bool = True, config: dict[str, any] = None) -> bs4.BeautifulSoup | None:
    """
    Uses Selenium to scrape the Altiplan website (with the configurations given by a config)
    and returns the HTML as a BeautifulSoup object.

    :param verbose: A boolean indicating whether to print the status of the scraping process. Default is True.
    :param config: A dictionary containing the configurations for the scraping process.

    :return: A BeautifulSoup object containing the HTML of the Altiplan website.
    """
    # **Unpacking the config dictionary** #########################################################
    if config is None:
        config = toml.load("config.toml")

    save_html = config["settings"]["save_html"]
    url_login = config["settings"]["url_login"]
    url_schedule = config["settings"]["url_schedule"]
    js_id_department = config["settings"]["js_ID_department"]
    js_id_username = config["settings"]["js_ID_username"]
    js_id_password = config["settings"]["js_ID_password"]
    js_id_dropdown = config["settings"]["js_ID_dropdown"]
    js_dropdown_select = config["settings"]["js_dropdown_select"]  # <-- Odense O-amb select in dropdown
    js_xpath_unique_afterlogin_elem = config["settings"]["js_XPATH_unique_afterlogin_elem"]
    run_headless = config["settings"]["run_headless"]
    run_selenium_regardless = config["settings"]["run_selenium_regardless"]  # <-- togleable: run `selenium` if already fetched?
    ###############################################################################################

    html_save_path = get_html_save_path()
    if not run_selenium_regardless and os.path.exists(html_save_path):
        if verbose:
            print("HTML already fetched.")
        with open(html_save_path, "r", encoding="utf-8") as file:
            return bs4.BeautifulSoup(file.read(), "html.parser")

    # Get credentials from .env file
    load_dotenv()  # <-- loads the .env file

    username = os.getenv("USERID")
    password = os.getenv("PASSWORD")
    department = os.getenv("DEPARTMENT")

    # Initialize Chrome options (optional: run in headless mode)
    options = Options()
    options.headless = run_headless

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url_login)  # <-- open login page

        # Wait until the input fields are present
        wait = WebDriverWait(driver, 10)
        afd_input = wait.until(ec.presence_of_element_located((By.ID, js_id_department)))
        brugernavn_input = driver.find_element(By.ID, js_id_username)
        password_input = driver.find_element(By.ID, js_id_password)

        # Input your credentials
        afd_input.send_keys(department)
        brugernavn_input.send_keys(username)
        password_input.send_keys(password)

        # Submit via submit-button
        submit_button = driver.find_element(By.NAME, "submitButton")
        submit_button.click()

        # Wait for the login process to complete
        wait.until(ec.presence_of_element_located((By.XPATH, js_xpath_unique_afterlogin_elem)))

        if verbose:
            print("Login successful.")

        # Navigate to the target page
        driver.get(url_schedule)

        # Wait until the target page loads
        wait.until(ec.presence_of_element_located((By.ID, js_id_dropdown)))

        # Select the desired option from the dropdown
        dropdown = Select(driver.find_element(By.ID, js_id_dropdown))
        dropdown.select_by_value(js_dropdown_select)

        # Wait for the page to update after selecting the dropdown option
        time.sleep(2)
        wait.until(ec.presence_of_element_located((By.TAG_NAME, "body")))

        if verbose:
            print("Page loaded. Scraping...")

        # Scrape the required data
        soup = bs4.BeautifulSoup(driver.page_source, "html.parser")

        if save_html:
            with open(html_save_path, "w", encoding="utf-8") as file:
                file.write(str(soup))

        return soup

    except Exception as e:
        driver.quit()
        print(f"An error occurred!!: {e}")
        return None

    finally:
        # Close the browser
        driver.quit()
