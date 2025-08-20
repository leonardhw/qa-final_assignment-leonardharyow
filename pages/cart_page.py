from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """
    Cart Page Object - Handles checkout functionality
    
    Note: Cart item management (add/reduce/remove) is handled by DashboardPage methods:
    - dashboard_page.add_first_product_to_cart()
    - dashboard_page.increase_cart_item_quantity(index)
    - dashboard_page.reduce_cart_item_quantity(index) 
    - dashboard_page.remove_cart_item(index)
    - dashboard_page.get_cart_item_quantity_text(index)
    """
    
    # Checkout functionality
    CHECKOUT_BUTTON = (By.XPATH, '//*[@id="root"]/div/main/div/div[2]/div/div[3]/button')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def proceed_to_checkout(self):
        """Click the checkout button to open checkout modal"""
        if self.is_element_visible(self.CHECKOUT_BUTTON):
            self.click_element(self.CHECKOUT_BUTTON)
            return True
        return False