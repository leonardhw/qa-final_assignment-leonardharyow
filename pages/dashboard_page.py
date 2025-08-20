from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):
    # Locators - Updated based on actual POS application structure
    # Product Search & Filter
    PRODUCT_SEARCH = (By.XPATH, '//*[@id="root"]/div/main/div/div[1]/div[1]/div/div/div/input')
    CATEGORY_SELECT = (By.XPATH, '//*[@id="root"]/div/main/div/div[1]/div[1]/div/select')
    
    # Product Catalog
    PRODUCT_CATALOG = (
        By.CSS_SELECTOR,
        "div.grid.grid-cols-2.md\:grid-cols-3.lg\:grid-cols-4.gap-4",
    )
    PRODUCT_ITEMS = (By.CSS_SELECTOR, "div.bg-white.rounded-lg.shadow-md.border")
    
    # Product Actions (for first product - can be dynamic)
    ADD_TO_CART_BUTTON_FIRST = (By.XPATH, '//*[@id="root"]/div/main/div/div[1]/div[2]/div/div[1]/div/button')
    
    # Cart Management (base patterns - will be made dynamic)
    CART_ITEM_BASE_PATH = '//*[@id="root"]/div/main/div/div[2]/div/div[2]/div[{}]/div[1]/div[2]'
    
    # Navigation
    LOGOUT_BUTTON = (By.XPATH, '//*[@id="root"]/div/div/div[3]/button')
    REPORTS_MENU = (By.XPATH, '//*[@id="root"]/div/div/nav/ul/li[4]/button')

    def __init__(self, driver):
        super().__init__(driver)

    def is_dashboard_loaded(self):
        return self.is_element_visible(self.PRODUCT_CATALOG) or self.is_element_visible(
            self.PRODUCT_SEARCH
        )

    def search_product(self, product_name):
        if self.is_element_visible(self.PRODUCT_SEARCH):
            self.send_keys_to_element(self.PRODUCT_SEARCH, product_name)

    def get_product_items(self):
        return self.find_elements(self.PRODUCT_ITEMS)

    def select_product_by_index(self, index):
        products = self.get_product_items()
        if index < len(products):
            products[index].click()
            return True
        return False

    def select_category(self, category_value):
        """Select a category from the dropdown filter"""
        if self.is_element_visible(self.CATEGORY_SELECT):
            from selenium.webdriver.support.ui import Select
            category_dropdown = self.find_element(self.CATEGORY_SELECT)
            select = Select(category_dropdown)
            select.select_by_visible_text(category_value)
    
    def add_first_product_to_cart(self):
        """Add the first product to cart using the provided XPath"""
        if self.is_element_visible(self.ADD_TO_CART_BUTTON_FIRST):
            self.click_element(self.ADD_TO_CART_BUTTON_FIRST)
            return True
        return False
    
    def add_product_to_cart_by_index(self, product_index):
        """Add a specific product to cart by index (0-based)"""
        # Dynamic XPath for different products
        product_xpath = f'//*[@id="root"]/div/main/div/div[1]/div[2]/div/div[{product_index + 1}]/div/button'
        product_locator = (By.XPATH, product_xpath)
        
        if self.is_element_visible(product_locator):
            self.click_element(product_locator)
            return True
        return False

    def click_reports_menu(self):
        if self.is_element_visible(self.REPORTS_MENU):
            self.click_element(self.REPORTS_MENU)
            return True
        return False

    def logout(self):
        if self.is_element_visible(self.LOGOUT_BUTTON):
            self.click_element(self.LOGOUT_BUTTON)
    
    # Cart Management Methods
    def get_cart_item_reduce_button(self, item_index):
        """Get the reduce (-) button for a specific cart item (0-based index)"""
        cart_item_path = self.CART_ITEM_BASE_PATH.format(item_index + 1)
        reduce_button_xpath = f'{cart_item_path}/div/button[1]'
        return (By.XPATH, reduce_button_xpath)
    
    def get_cart_item_add_button(self, item_index):
        """Get the add (+) button for a specific cart item (0-based index)"""
        cart_item_path = self.CART_ITEM_BASE_PATH.format(item_index + 1)
        add_button_xpath = f'{cart_item_path}/div/button[2]'
        return (By.XPATH, add_button_xpath)
    
    def get_cart_item_remove_button(self, item_index):
        """Get the remove button for a specific cart item (0-based index)"""
        cart_item_path = self.CART_ITEM_BASE_PATH.format(item_index + 1)
        remove_button_xpath = f'{cart_item_path}/button'
        return (By.XPATH, remove_button_xpath)
    
    def get_cart_item_quantity(self, item_index):
        """Get the quantity span for a specific cart item (0-based index)"""
        cart_item_path = self.CART_ITEM_BASE_PATH.format(item_index + 1)
        quantity_xpath = f'{cart_item_path}/div/span'
        return (By.XPATH, quantity_xpath)
    
    def reduce_cart_item_quantity(self, item_index):
        """Reduce quantity of a specific cart item by 1"""
        reduce_button = self.get_cart_item_reduce_button(item_index)
        if self.is_element_visible(reduce_button):
            self.click_element(reduce_button)
            return True
        return False
    
    def increase_cart_item_quantity(self, item_index):
        """Increase quantity of a specific cart item by 1"""
        add_button = self.get_cart_item_add_button(item_index)
        if self.is_element_visible(add_button):
            self.click_element(add_button)
            return True
        return False
    
    def remove_cart_item(self, item_index):
        """Remove a specific cart item completely"""
        remove_button = self.get_cart_item_remove_button(item_index)
        if self.is_element_visible(remove_button):
            self.click_element(remove_button)
            return True
        return False
    
    def get_cart_item_quantity_text(self, item_index):
        """Get the quantity text for a specific cart item"""
        quantity_locator = self.get_cart_item_quantity(item_index)
        if self.is_element_visible(quantity_locator):
            return self.get_element_text(quantity_locator)
        return None
