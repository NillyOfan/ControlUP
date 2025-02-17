from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import logging

logger = logging.getLogger(__name__)

class BasePage:
    """A base class for all pages, containing common web interactions."""

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 10)

    def open_url(self):
        """Opens the given URL."""
        logger.debug(f"Opening URL: {self.url}")
        try:
            self.driver.get(self.url)
        except WebDriverException as e:
            logger.error(f"Failed to open URL {self.url}: {str(e)}")

    def find_element(self, by, locator):
        """Finds a single element on the page."""
        try:
            element = self.wait.until(EC.presence_of_element_located((by, locator)))
            logger.debug(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Timeout: Element not found: {locator}")
            return None

    def find_elements(self, by, locator):
        """Finds multiple elements on the page."""
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located((by, locator)))
            logger.debug(f"Elements found: {locator}")
            return elements
        except TimeoutException:
            logger.error(f"Timeout: Elements not found: {locator}")
            return []

    def click_element(self, by, locator):
        """Clicks an element on the page."""
        element = self.find_element(by, locator)
        if element:
            element.click()
            logger.debug(f"Clicked element: {locator}")

    def enter_text(self, by, locator, text):
        """Enters text into an input field."""
        element = self.find_element(by, locator)
        if element:
            element.clear()
            element.send_keys(text)
            logger.debug(f"Entered text '{text}' into element: {locator}")

    def get_element_text(self, by, locator):
        """Gets text from an element."""
        element = self.find_element(by, locator)
        return element.text if element else ""

    def is_element_visible(self, by, locator):
        """Checks if an element is visible."""
        try:
            element = self.wait.until(EC.visibility_of_element_located((by, locator)))
            return bool(element)
        except TimeoutException:
            return False
