import os
from dataclasses import dataclass


@dataclass
class Config:
    BASE_URL: str = "https://simple-pos-pwdk.netlify.app/"
    BROWSER: str = "chrome"
    HEADLESS: bool = False
    IMPLICIT_WAIT: int = 10
    EXPLICIT_WAIT: int = 20

    # Test credentials
    ADMIN_EMAIL: str = "admin@pos.com"
    ADMIN_PASSWORD: str = "admin"

    # Paths
    TEST_DATA_PATH: str = os.path.join(os.path.dirname(__file__), "..", "data")
    REPORTS_PATH: str = os.path.join(os.path.dirname(__file__), "..", "reports")
    SCREENSHOTS_PATH: str = os.path.join(REPORTS_PATH, "screenshots")


# Create instance
config = Config()
