import pytest
import allure
import os
import logging
import yaml
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tempfile


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "config.yaml")

if not os.path.isfile(CONFIG_PATH):
    raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

log_filename = config["logging"].get("file") or f"test_execution_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
LOG_FILE_PATH = os.path.join(LOGS_DIR, log_filename)


def setup_logger():
    # """Set up centralized logging once per test session."""

    logging.basicConfig(
        level=logging.getLevelName(config["logging"].get("level", "INFO").upper()),
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger()


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Ensure logging is set up when pytest starts."""
    global logger  # Make logger accessible globally
    logger = setup_logger()

def get_chrome_driver():
    """Returns a configured Chrome WebDriver instance."""
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")  # Ensure it's running headless in CI/CD
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")  # Unique temp directory to prevent conflicts

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

@pytest.fixture(scope="function")
def driver():
    """Fixture to initialize and quit WebDriver."""
    logger.info("Initializing WebDriver")
    driver = get_chrome_driver()
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
    report_dir = os.path.join(PROJECT_ROOT,"reports")
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
