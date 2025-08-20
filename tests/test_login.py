import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.data_reader import DataReader

class TestLogin:
    
    @pytest.mark.high
    def test_valid_login(self, setup_teardown, test_credentials):
        """TC_001: Login with valid credentials"""
        driver = setup_teardown
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        
        # Perform login with valid credentials
        login_page.login(test_credentials["valid_email"], test_credentials["valid_password"])
        
        # Verify successful login
        assert login_page.is_login_successful(), f"Login should be successful with valid credentials (email: {test_credentials['valid_email']}) but failed"
        assert dashboard_page.is_dashboard_loaded(), "Dashboard should be loaded after successful login but dashboard elements are not visible"
    
    @pytest.mark.high  
    def test_logout_functionality(self, setup_teardown, test_credentials):
        """TC_003: Logout from application"""
        driver = setup_teardown
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        
        # First login
        login_page.login(test_credentials["valid_email"], test_credentials["valid_password"])
        assert login_page.is_login_successful(), "Initial login should be successful before testing logout functionality"
        
        # Perform logout
        dashboard_page.logout()
        
        # Verify logout successful - should be back on login page
        assert login_page.is_on_login_page(), f"Should be redirected to login page after logout but current URL is: {login_page.get_current_url()}"
    
    @pytest.mark.medium
    def test_invalid_login_credentials(self, setup_teardown):
        """TC_002: Login with invalid credentials should show error message"""
        driver = setup_teardown
        login_page = LoginPage(driver)
        
        # Get test data from CSV
        test_data = DataReader.get_login_test_case("invalid_login")
        email = test_data['email']
        password = test_data['password']
        expected_result = test_data['expected_result']
        
        # Attempt login with invalid credentials from CSV
        login_page.login(email, password)
        
        # Wait for error message to appear
        time.sleep(3)
        
        if expected_result == "failure":
            # Verify login failed (should still be on login page)
            assert login_page.is_on_login_page(), f"Should still be on login page after invalid login (email: {email}) but was redirected to: {login_page.get_current_url()}"
            
            # Verify error message is displayed
            error_message = login_page.get_error_message()
            assert error_message is not None, f"Error message should be displayed for invalid credentials (email: {email}, password: {password}) but no error message found"
            assert "Invalid credentials" in error_message, f"Error message should contain 'Invalid credentials' for failed login attempt. Got: {error_message}"