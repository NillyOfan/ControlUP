import pytest
from pages.store_page import StorePage
import logging

logger = logging.getLogger(__name__)


@pytest.fixture
def store_page(driver):
    """Fixture to initialize StorePage."""
    page = StorePage(driver, "https://www.saucedemo.com")
    logger.info("Logging into the store")
    page.login("standard_user", "secret_sauce")
    return page


def test_inventory_items_count(store_page):
    """Scenario: Verify Inventory Items"""
    logger.info("Retrieving inventory items")
    inventory_items = store_page.get_inventory_items()

    assert len(inventory_items) == 6, f"Expected 6 items, but found {len(inventory_items)}"


def test_add_item_to_cart(store_page):
    """Scenario: Add Item to Cart"""
    logger.info("Adding first item to the cart")
    store_page.add_first_item_to_cart()

    cart_count = store_page.get_cart_count()
    logger.info(f"Cart count after adding item: {cart_count}")

    assert cart_count == 1, f"Expected cart count to be 1, but got {cart_count}"
