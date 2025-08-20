from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Locators
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "div.bg-red-50.border.border-red-200.text-red-600")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_login_page(self):
        self.driver.get("https://simple-pos-pwdk.netlify.app/")
    
    def enter_email(self, email):
        self.send_keys_to_element(self.EMAIL_INPUT, email)
    
    def enter_password(self, password):
        self.send_keys_to_element(self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
    
    def is_login_successful(self):
        # Check if redirected to dashboard/main page
        return "dashboard" in self.get_current_url().lower() or \
               "pos" in self.get_current_url().lower() or \
               self.get_current_url() != "https://simple-pos-pwdk.netlify.app/"
    
    def get_error_message(self):
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_element_text(self.ERROR_MESSAGE)
        return None
    
    def is_on_login_page(self):
        return self.is_element_visible(self.LOGIN_BUTTON) and \
               self.is_element_visible(self.EMAIL_INPUT)