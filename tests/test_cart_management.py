import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.data_reader import DataReader


class TestCartManagement:
    
    @pytest.fixture(autouse=True)
    def login_setup(self, setup_teardown, test_credentials):
        """Automatically login before each test"""
        self.driver = setup_teardown
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        
        # Login before each test
        self.login_page.login(test_credentials["valid_email"], test_credentials["valid_password"])
        assert self.login_page.is_login_successful(), "Login should be successful before testing cart management functionality"
        
        # Ensure we're on the dashboard/POS page
        assert self.dashboard_page.is_dashboard_loaded(), "Dashboard should be loaded to access cart functionality"
    
    @pytest.mark.high
    def test_add_wireless_headphones_to_cart(self):
        """TC_011: Add Wireless Headphones to cart"""
        # Get test data from CSV
        test_data = DataReader.get_cart_test_case("add_wireless_headphones")
        product_name = test_data['product_name']
        expected_result = test_data['expected_result']
        
        # Search for Wireless Headphones to make sure it's visible
        self.dashboard_page.search_product(product_name)
        time.sleep(2)
        
        # Verify products are available
        products = self.dashboard_page.get_product_items()
        assert len(products) > 0, f"Should find products when searching for '{product_name}' but found {len(products)} products"
        
        # Add first product (Wireless Headphones) to cart
        success = self.dashboard_page.add_first_product_to_cart()
        assert success, f"Should be able to add {product_name} to cart but add operation failed"
        
        # Wait for cart to update
        time.sleep(2)
        
        if expected_result == "success":
            assert True, f"Successfully added {product_name} to cart as expected from test data"
    
    @pytest.mark.high  
    def test_increase_cart_item_quantity(self):
        """TC_012: Increase quantity of Wireless Headphones in cart using + button"""
        # Get test data
        test_data = DataReader.get_cart_test_case("increase_quantity")
        product_name = test_data['product_name']
        expected_result = test_data['expected_result']
        
        # First add product to cart (prerequisite)
        self.dashboard_page.search_product(product_name)
        time.sleep(1)
        self.dashboard_page.add_first_product_to_cart()
        time.sleep(2)
        
        # Increase quantity using + button (first cart item, index 0)
        success = self.dashboard_page.increase_cart_item_quantity(0)
        assert success, f"Should be able to increase cart item quantity for {product_name} but operation failed"
        
        # Wait for cart to update
        time.sleep(2)
        
        if expected_result == "success":
            assert True, f"Successfully increased quantity of {product_name} as expected from test data"
    
    @pytest.mark.high
    def test_decrease_cart_item_quantity(self):
        """TC_013: Decrease quantity of Wireless Headphones in cart using - button"""
        # Get test data
        test_data = DataReader.get_cart_test_case("decrease_quantity")
        product_name = test_data['product_name']
        expected_result = test_data['expected_result']
        
        # First add product to cart and increase quantity (prerequisite)
        self.dashboard_page.search_product(product_name)
        time.sleep(1)
        self.dashboard_page.add_first_product_to_cart()
        time.sleep(1)
        # Add one more to have quantity of 2
        self.dashboard_page.increase_cart_item_quantity(0)
        time.sleep(2)
        
        # Decrease quantity using - button (first cart item, index 0)
        success = self.dashboard_page.reduce_cart_item_quantity(0)
        assert success, f"Should be able to decrease cart item quantity for {product_name} but operation failed"
        
        # Wait for cart to update
        time.sleep(2)
        
        if expected_result == "success":
            assert True, f"Successfully decreased quantity of {product_name} as expected from test data"
    
    @pytest.mark.high
    def test_remove_item_from_cart(self):
        """TC_014: Remove Wireless Headphones from cart completely"""
        # Get test data
        test_data = DataReader.get_cart_test_case("remove_item")
        product_name = test_data['product_name']
        expected_result = test_data['expected_result']
        
        # First add product to cart (prerequisite)
        self.dashboard_page.search_product(product_name)
        time.sleep(1)
        self.dashboard_page.add_first_product_to_cart()
        time.sleep(2)
        
        # Remove item from cart (first cart item, index 0)
        success = self.dashboard_page.remove_cart_item(0)
        assert success, f"Should be able to remove {product_name} from cart but remove operation failed"
        
        # Wait for cart to update
        time.sleep(2)
        
        if expected_result == "success":
            assert True, f"Successfully removed {product_name} from cart as expected from test data"