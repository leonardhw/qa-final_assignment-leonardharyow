import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.reports_page import ReportsPage
from utils.data_reader import DataReader


class TestReports:

    @pytest.fixture(autouse=True)
    def login_setup(self, setup_teardown, test_credentials):
        """Automatically login before each test"""
        self.driver = setup_teardown
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.checkout_page = CheckoutPage(self.driver)
        self.reports_page = ReportsPage(self.driver)

        # Login before each test
        self.login_page.login(
            test_credentials["valid_email"], test_credentials["valid_password"]
        )
        assert self.login_page.is_login_successful(), "Login should be successful before testing reports functionality"

        # Ensure we're on the dashboard/POS page
        assert self.dashboard_page.is_dashboard_loaded(), "Dashboard should be loaded to access reports functionality"

    @pytest.mark.high
    def test_complete_transaction_and_verify_using_helper_method(self):
        """TC_016: Complete transaction and verify reports using helper verification method"""
        # Get test data
        test_data = DataReader.get_reports_test_case("after_single_transaction")

        # Get checkout data
        checkout_data = DataReader.get_checkout_test_case("complete_checkout_card")

        # Complete the full workflow: Add to cart → Checkout → Verify Reports
        # Step 1: Setup and complete transaction
        self.dashboard_page.search_product("Wireless Headphones")
        time.sleep(2)
        self.dashboard_page.add_first_product_to_cart()
        time.sleep(2)

        # Complete checkout
        self.cart_page.proceed_to_checkout()
        time.sleep(3)
        transaction_success, message = self.checkout_page.complete_checkout_transaction(
            checkout_data["customer_name"],
            checkout_data["customer_email"],
            checkout_data["notes"],
        )
        assert transaction_success, f"Transaction should complete successfully before verifying reports but failed: {message}"
        time.sleep(3)

        # Step 2: Navigate to reports and verify using helper method
        self.dashboard_page.click_reports_menu()
        time.sleep(3)

        # Use the comprehensive verification helper method
        verification_results = self.reports_page.verify_reports_data(
            test_data["expected_total_sales"],
            test_data["expected_transactions"],
            test_data["expected_average_order"],
            test_data["expected_top_products_count"],
            test_data["expected_product"],
        )

        # Assert all verifications passed
        assert verification_results["page_loaded"], "Reports page should be loaded but page load verification failed"
        assert verification_results[
            "correct_heading"
        ], "Should have correct 'Sales Reports' heading but heading verification failed"
        assert verification_results[
            "total_sales_match"
        ], f"Total sales should match expected value. Expected: {test_data['expected_total_sales']}, Got: {verification_results['actual_values']['total_sales']}"
        assert verification_results[
            "transactions_match"
        ], f"Transactions count should match expected value. Expected: {test_data['expected_transactions']}, Got: {verification_results['actual_values']['transactions']}"
        assert verification_results[
            "average_order_match"
        ], f"Average order should match expected value. Expected: {test_data['expected_average_order']}, Got: {verification_results['actual_values']['average_order']}"
        assert verification_results[
            "top_products_count_match"
        ], f"Top products count should match expected value. Expected: {test_data['expected_top_products_count']}, Got: {verification_results['actual_values']['top_products_count']}"
        assert verification_results[
            "product_in_list"
        ], f"Product '{test_data['expected_product']}' should be present in Top Products list but was not found"

        # Print verification results for debugging
        print(f"Verification Results: {verification_results}")

        assert (
            True
        ), "Successfully completed transaction and verified all reports data using helper method"

    @pytest.mark.medium
    def test_navigate_to_reports_page(self):
        """TC_017: Simple navigation to reports page verification"""
        # Navigate to Reports page
        self.dashboard_page.click_reports_menu()

        # Wait for page to load
        time.sleep(3)

        # Verify we're on the Reports page
        on_reports_page = self.reports_page.is_on_reports_page()
        assert on_reports_page, "Should be on Reports page after navigation but page verification failed"

        # Verify the heading
        heading = self.reports_page.get_reports_heading_text()
        assert (
            heading == "Sales Reports"
        ), f"Should see 'Sales Reports' heading but got: '{heading}'"

        # Verify page elements are present (even if showing zero values)
        total_sales = self.reports_page.get_total_sales()
        transactions = self.reports_page.get_transactions_count()
        average_order = self.reports_page.get_average_order()
        top_products_count = self.reports_page.get_top_products_count()

        # All elements should return some value (even if $0.00 or 0)
        assert total_sales is not None, "Total sales element should be present on reports page but was not found"
        assert transactions is not None, "Transactions element should be present on reports page but was not found"
        assert average_order is not None, "Average order element should be present on reports page but was not found"
        assert (
            top_products_count is not None
        ), "Top products count element should be present on reports page but was not found"

        print(
            f"Reports page values - Total Sales: {total_sales}, Transactions: {transactions}, Average Order: {average_order}, Top Products: {top_products_count}"
        )

        assert True, "Successfully navigated to Reports page and verified page elements"
