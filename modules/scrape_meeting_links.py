# Built in modules
import re, logging, time, random
from datetime import datetime, timedelta

# External modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementClickInterceptedException,
)
from bs4 import BeautifulSoup


# Input dates are strings of such format: 2023-12-30
def scrape_meeting_links(start_date_str, end_date_str):
    # Convert string to date objects and checking validity
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    delta = end_date - start_date
    if delta < timedelta(days=0):
        logging.error("Start date must be earlier than end date")
        raise Exception("Start date must be earlier than end date")

    # Sets driver options
    options = Options()
    options.page_load_strategy = (
        "normal"  # Makes the driver wait until all resources are downloaded
    )
    options.add_argument(
        "--headless=new"
    )  # Use the new headless feature of Chromium based browsers

    # Starts driver session and loads council meetings spa
    driver = webdriver.Chrome(options=options)
    meeting_spa_url = (
        "https://covapp.vancouver.ca/councilMeetingPublic/CouncilMeetings.aspx"
    )
    driver.get(meeting_spa_url)
    # Goes to the page where scrapping begins
    driver.find_element(By.LINK_TEXT, "By Date").click()
    try:
        # The page is loaded when this (from date field) becomes clickable
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.ID, "LiverpoolTheme_wt93_block_wtMainContent_wttxtFromDate")
            )
        )
    except TimeoutException:
        driver.quit()
        logging.error(f"The page {meeting_spa_url} did not load")
        raise TimeoutException(f"The page {meeting_spa_url} did not load")

    # Chunking 90 days at a time
    range_start_date = start_date
    range_end_date = end_date
    if range_start_date + timedelta(days=90) < end_date:
        range_end_date = range_start_date + timedelta(days=90)
    while True:
        # Code for scraping
        logging.info(
            f"Scraping meeting links from {str(range_start_date)} to {str(range_end_date)}."
        )
        time.sleep(random.randint(5, 10))

        driver.find_element(
            By.ID, "LiverpoolTheme_wt93_block_wtMainContent_wttxtFromDate"
        ).clear()
        driver.find_element(
            By.ID, "LiverpoolTheme_wt93_block_wtMainContent_wttxtFromDate"
        ).send_keys(str(range_start_date))
        driver.find_element(
            By.ID, "LiverpoolTheme_wt93_block_wtMainContent_wttxtToDate"
        ).clear()
        driver.find_element(
            By.ID, "LiverpoolTheme_wt93_block_wtMainContent_wttxtToDate"
        ).send_keys(str(range_end_date))

        try:
            driver.find_element(By.XPATH, "//input[@value='Display']").click()
        # Incase the the seleniumn cannot click, clicks via JavaScript.
        # Probably some inconsistancy with the SPA
        except ElementClickInterceptedException:
            logging.warning(
                f"ElementClickInterceptedException when clicking Display for {str(range_start_date)} to {str(range_end_date)}"
            )
            driver.execute_script(
                "arguments[0].click();",
                driver.find_element(By.XPATH, "//input[@value='Display']"),
            )

        # SPA loaded the range of dates. Yields link urls
        while True:
            try:
                WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//a[contains(@href, 'ag.htm')]")
                    )
                )
            except TimeoutException:
                logging.info(
                    f"No meetings found between {str(range_start_date)} and {str(range_end_date)}."
                )
            else:
                soup = BeautifulSoup(driver.page_source, "html.parser")
                for link in soup.find_all("a", href=re.compile("ag\.htm$")):
                    yield link["href"]

                try:
                    time.sleep(random.randint(5, 10))
                    next_button = driver.find_element(By.LINK_TEXT, "next")
                except NoSuchElementException:
                    logging.info(
                        f"Done scraping meeting links from {str(range_start_date)} to {str(range_end_date)}."
                    )
                    break
                else:
                    next_button.click()
                    logging.info("Next button clicked")
                    # Waits until next page is loaded
                    WebDriverWait(driver, 3).until(EC.staleness_of(next_button))

        # Set range for next iteration or break if at end
        range_start_date = range_end_date + timedelta(days=1)
        if range_start_date > end_date:
            break
        else:
            range_end_date = end_date
            if range_start_date + timedelta(days=90) < end_date:
                range_end_date = range_start_date + timedelta(days=90)

    driver.quit()
