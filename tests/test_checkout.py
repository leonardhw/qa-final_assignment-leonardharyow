import pytest
import time
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data_reader import DataReader


class TestCheckout:

    @pytest.fixture(autouse=True)
    def login_and_cart_setup(self, setup_teardown, test_credentials):
        """Automatically login and setup cart with Wireless Headphones before each test"""
        self.driver = setup_teardown
        self.login_page = LoginPage(self.driver)
        self.dashboard_page = DashboardPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.checkout_page = CheckoutPage(self.driver)

        # Login before each test
        self.login_page.login(
            test_credentials["valid_email"], test_credentials["valid_password"]
        )
        assert self.login_page.is_login_successful(), "Login should be successful before testing checkout functionality"

        # Ensure we're on the dashboard/POS page
        assert self.dashboard_page.is_dashboard_loaded(), "Dashboard should be loaded to access checkout functionality"

        # Setup cart with Wireless Headphones (prerequisite for checkout)
        self.dashboard_page.search_product("Wireless Headphones")
        time.sleep(2)

        # Verify products are available
        products = self.dashboard_page.get_product_items()
        assert len(products) > 0, f"Should find Wireless Headphones for checkout test but found {len(products)} products"

        # Add Wireless Headphones to cart
        success = self.dashboard_page.add_first_product_to_cart()
        assert (
            success
        ), "Should be able to add Wireless Headphones to cart for checkout test but add operation failed"
        time.sleep(2)

    # @pytest.mark.high
    # def test_complete_checkout_with_card_payment(self):
    #     """TC_018: Complete checkout process with Card payment and verify success alert"""
    #     # Get test data from CSV
    #     test_data = DataReader.get_checkout_test_case("complete_checkout_card")
    #     customer_name = test_data["customer_name"]
    #     customer_email = test_data["customer_email"]
    #     payment_method = test_data["payment_method"]
    #     notes = test_data["notes"]
    #     expected_result = test_data["expected_result"]

    #     # Step 1: Click checkout button to open checkout modal
    #     checkout_opened = self.cart_page.proceed_to_checkout()
    #     assert checkout_opened, "Should be able to click checkout button"

    #     # Wait for checkout modal to load
    #     time.sleep(3)

    #     # Step 2: Verify checkout modal is open
    #     modal_open = self.checkout_page.is_checkout_modal_open()
    #     assert modal_open, "Checkout modal should be open"

    #     # Step 3: Fill customer name
    #     name_entered = self.checkout_page.enter_customer_name(customer_name)
    #     assert name_entered, f"Should be able to enter customer name: {customer_name}"
    #     time.sleep(1)

    #     # Step 4: Fill customer email
    #     email_entered = self.checkout_page.enter_customer_email(customer_email)
    #     assert (
    #         email_entered
    #     ), f"Should be able to enter customer email: {customer_email}"
    #     time.sleep(1)

    #     # Step 5: Select Card payment method
    #     card_selected = self.checkout_page.select_card_payment()
    #     assert (
    #         card_selected
    #     ), f"Should be able to select {payment_method} payment method"
    #     time.sleep(1)

    #     # Step 6: Fill notes
    #     notes_entered = self.checkout_page.enter_notes(notes)
    #     assert notes_entered, f"Should be able to enter notes: {notes}"
    #     time.sleep(1)

    #     # Step 7: Click Complete Transaction button
    #     transaction_clicked = self.checkout_page.click_complete_transaction()
    #     assert (
    #         transaction_clicked
    #     ), "Should be able to click Complete Transaction button"

    #     # Step 8: Wait for and handle success alert
    #     alert_appeared = self.checkout_page.wait_for_alert(timeout=10)
    #     assert (
    #         alert_appeared
    #     ), "Success alert should appear after transaction completion"

    #     # Step 9: Get alert text and verify success message
    #     alert_text = self.checkout_page.get_alert_text()
    #     assert alert_text is not None, "Should be able to get alert text"
    #     assert (
    #         "Transaction completed successfully" in alert_text
    #     ), f"Alert should contain success message. Got: {alert_text}"

    #     # Step 10: Accept the alert (click OK)
    #     alert_accepted = self.checkout_page.accept_alert()
    #     assert alert_accepted, "Should be able to accept success alert"

    #     # Wait for alert to be dismissed
    #     time.sleep(2)

    #     if expected_result == "success":
    #         assert (
    #             True
    #         ), f"Successfully completed checkout with {payment_method} payment for {customer_name}"

    @pytest.mark.high
    def test_complete_checkout_using_helper_method(self):
        """TC_015: Complete checkout using the helper method for streamlined testing"""
        # Get test data
        test_data = DataReader.get_checkout_test_case("complete_checkout_card")
        customer_name = test_data["customer_name"]
        customer_email = test_data["customer_email"]
        notes = test_data["notes"]

        # Click checkout to open modal
        checkout_opened = self.cart_page.proceed_to_checkout()
        assert checkout_opened, "Should be able to open checkout modal but checkout button click failed"
        time.sleep(3)

        # Use the complete checkout helper method
        success, message = self.checkout_page.complete_checkout_transaction(
            customer_name, customer_email, notes
        )

        assert success, f"Checkout should complete successfully but failed. Error message: {message}"
        assert (
            "Transaction completed successfully" in message
        ), f"Should get 'Transaction completed successfully' message but got: {message}"
