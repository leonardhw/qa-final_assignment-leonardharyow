import pytest
import os
from utils.driver_manager import DriverManager
from config.config import config

@pytest.fixture(scope="session")
def driver():
    driver = DriverManager.get_driver()
    yield driver
    DriverManager.quit_driver()

@pytest.fixture(scope="function")
def setup_teardown(driver):
    # Setup: Navigate to base URL
    driver.get(config.BASE_URL)
    yield driver
    # Teardown: Clear cookies and local storage
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")

@pytest.fixture
def test_credentials():
    return {
        "valid_email": config.ADMIN_EMAIL,
        "valid_password": config.ADMIN_PASSWORD,
        "invalid_email": "invalid@test.com",
        "invalid_password": "wrongpassword"
    }

def pytest_configure(config):
    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Create screenshots directory
    screenshots_dir = os.path.join(reports_dir, "screenshots")
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    
    # Set a report attribute for each phase of a call, which can be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope="function", autouse=True)
def screenshot_on_failure(request, driver):
    yield
    # Check if test failed
    if request.node.rep_call.failed:
        # Take screenshot
        screenshot_dir = os.path.join(os.path.dirname(__file__), "reports", "screenshots")
        screenshot_name = f"{request.node.name}_{request.node.rep_call.when}.png"
        screenshot_path = os.path.join(screenshot_dir, screenshot_name)
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")