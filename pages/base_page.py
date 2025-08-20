from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.config import config

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)
    
    def find_element(self, locator):
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise NoSuchElementException(f"Element {locator} not found")
    
    def find_elements(self, locator):
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []
    
    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def send_keys_to_element(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_element_text(self, locator):
        element = self.find_element(locator)
        return element.text
    
    def is_element_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator):
        try:
            self.find_element(locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_element_to_disappear(self, locator):
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            pass
    
    def get_current_url(self):
        return self.driver.current_url
    
    def get_page_title(self):
        return self.driver.title
    
    # Alert handling methods
    def wait_for_alert(self, timeout=10):
        """Wait for browser alert to appear"""
        try:
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            return True
        except TimeoutException:
            return False
    
    def get_alert_text(self):
        """Get text from browser alert"""
        try:
            alert = self.driver.switch_to.alert
            return alert.text
        except:
            return None
    
    def accept_alert(self):
        """Click OK on browser alert"""
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            return True
        except:
            return False
    
    def dismiss_alert(self):
        """Click Cancel on browser alert"""
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
            return True
        except:
            return False