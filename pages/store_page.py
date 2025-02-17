from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class StorePage(BasePage):
    """Page Object Model for an online store. Supports dynamic store customization."""

    def __init__(self, driver, url, locators=None):
        """
        Initialize StorePage with a specific store URL and dynamic locators.
        Defaults to SauceDemo's locators if none are provided.
        """
        super().__init__(driver, url)

        # Default locators (SauceDemo)
        default_locators = {
            "username_input": (By.ID, "user-name"),
            "password_input": (By.ID, "password"),
            "login_button": (By.ID, "login-button"),
            "inventory_item": (By.CLASS_NAME, "inventory_item"),
            "add_to_cart_button": (By.CSS_SELECTOR, ".inventory_item button"),
            "cart_badge": (By.CLASS_NAME, "shopping_cart_badge"),
        }

        # Merge custom locators (if provided) with defaults
        self.locators = {**default_locators, **(locators or {})}

    def login(self, username, password):
        """Logs into the store using the provided credentials."""
        logger.info("Logging in...")
        self.open_url()
        self.enter_text(*self.locators["username_input"], username)
        self.enter_text(*self.locators["password_input"], password)
        self.click_element(*self.locators["login_button"])

    def get_inventory_items(self):
        """Returns a list of inventory items."""
        logger.debug("Fetching inventory items...")
        return self.find_elements(*self.locators["inventory_item"])

    def add_first_item_to_cart(self):
        """Adds the first inventory item to the cart."""
        logger.debug("Adding first item to cart...")
        self.click_element(*self.locators["add_to_cart_button"])

    def get_cart_count(self):
        """Returns the number displayed in the cart badge."""
        cart_badge = self.find_element(*self.locators["cart_badge"])
        return int(cart_badge.text) if cart_badge else 0
