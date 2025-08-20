from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.config import config


class DriverManager:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            cls._driver = cls._create_driver()
        return cls._driver

    @classmethod
    def _create_driver(cls):
        if config.BROWSER.lower() == "chrome":
            chrome_options = Options()
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            if config.HEADLESS:
                chrome_options.add_argument("--headless")

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.implicitly_wait(config.IMPLICIT_WAIT)
            # driver.maximize_window()
            return driver
        else:
            raise ValueError(f"Browser {config.BROWSER} is not supported")

    @classmethod
    def quit_driver(cls):
        if cls._driver:
            cls._driver.quit()
            cls._driver = None
