import pytest
import allure
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import yaml
import datetime


# Get the absolute path of the project root (assuming conftest.py is inside tests/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"PROJECT_ROOT: {PROJECT_ROOT}")  # Debugging: Print log path
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "config.yaml")
print(f"CONFIG_PATH: {CONFIG_PATH}")  # Debugging: Print log path

# Verify the path before trying to open it
if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

# Load config
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

# Generate a unique log filename for each test session
log_filename = f"logs/test_execution_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
print(f"log_filename: {log_filename}")  # Debugging: Print log path
LOG_FILE_PATH = config["logging"].get("file", log_filename)  # Use config.yaml if exists, else use new filename
print(f"LOG_FILE_PATH: {LOG_FILE_PATH}")  # Debugging: Print log path

def setup_logger():
    """Set up centralized logging once per test session."""
    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set log level (DEBUG, INFO, WARNING, etc.)

    # Ensure logs directory exists
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

    # Remove existing handlers to prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    # File Handler
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    # Console Handler (optional)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    return logger  # Return the logger instance
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Ensure logging is set up when pytest starts."""
    global logger  # Make logger accessible globally
    logger = setup_logger()


@pytest.fixture(scope="session", autouse=True)
def initialize_logging():
    """Automatically initialize logging for all test sessions."""
    global logger
    logger = setup_logger()


@pytest.fixture(scope="function")
def driver():
    """Fixture to initialize and quit WebDriver."""
    logger.info("Initializing WebDriver")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield driver
    logger.info("Quitting WebDriver")
    driver.quit()

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Hook: Runs before each test setup."""
    logger.info(f"Setting up test: {item.name}")

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item):
    """Hook: Runs after each test teardown."""
    logger.info(f"Tearing down test: {item.name}")

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Hook: Captures test results and logs to Allure & Pytest report."""
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)  # Ensure 'reports' directory exists

    if call.when == "call":
        if call.excinfo is None:
            logger.info(f"Test Passed: {item.name}")
            allure.attach("Test Passed", name=item.name, attachment_type=allure.attachment_type.TEXT)
        else:
            logger.error(f"Test Failed: {item.name}")
            allure.attach("Test Failed", name=item.name, attachment_type=allure.attachment_type.TEXT)

    # Append logs to file for Pytest reporting
    with open(os.path.join(report_dir, "test_log.txt"), "a") as log_file:
        log_file.write(f"{item.name} - {'PASSED' if call.excinfo is None else 'FAILED'}\n")
